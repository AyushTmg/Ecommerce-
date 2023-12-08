from rest_framework import serializers
from .models import Product,Collection,Review,CartItem,Cart,Customer,Order,OrderItem,ProductImage
from decimal import Decimal
from django.db import transaction
from .signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']
    
    def create(self, validated_data):
        product_id=self.context['product_id']
        return ProductImage.objects.create(product_id=product_id,**validated_data)
class ProductSerializer(serializers.ModelSerializer):
    tax_amount=serializers.SerializerMethodField(method_name='get_tax_amount')
    image=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=['id','title','unit_price','inventory','tax_amount','collection','image']

    def get_tax_amount(self,product:Product):
        return product.unit_price*Decimal(1.2)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','date','description']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']


    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        print(f"product_id-->{product_id} and quantity-->{quantity}")

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
            
        return self.instance

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    price=serializers.SerializerMethodField(method_name='get_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','price']

    def get_price(self,cartitem:CartItem):
        return cartitem.product.unit_price*cartitem.quantity

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    item=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField('get_total_price')
    class Meta:
        model=Cart
        fields=['id','item','total_price']
    
    def get_total_price(self,cart:Cart): 
        return sum([items.quantity*items.product.unit_price for items in cart.item.all()])


class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    orderitem=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','placed_at','payment_status','orderitem']


class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
   
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id=self.validated_data['cart_id']
            (customer,created_at)=Customer.objects.get_or_create(user_id=self.context['user_id'])
            order=Order.objects.create(customer=customer)
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items=[
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity ,
                    unit_price=item.product.unit_price

                )

                    for item in cart_items]
            
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(id=cart_id).delete()

            order_created.send_robust(self.__class__,order=order)

            return order

        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta :
        model=Order
        fields=['payment_status']

