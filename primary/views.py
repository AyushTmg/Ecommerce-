from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartItemSerializer,\
CartSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,\
OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer,ProductImageSerializer
from .paginations import Default
from  .models import Product,Collection,OrderItem,Review,CartItem,Cart,Customer,Order,ProductImage
from .filters import ProductFilter
from .permissions import IsAdminOrReadonly




class ProductViewSet(ModelViewSet):
    queryset=Product.objects.select_related('collection').prefetch_related('image').all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['title']
    ordering_fields=['unit_price']
    pagination_class=Default
    permission_classes=[IsAdminOrReadonly]

    # def get_permissions(self):
    #     if self.request.method=='GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':"Cant be deleted"},status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer
    filter_backends=[SearchFilter]
    pagination_class=Default
    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        # print(self.kwargs)
        return Review.objects.filter(product_id= self.kwargs['products_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['products_pk']}



# class CartViewSet(ModelViewSet):
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Cart.objects.prefetch_related('item__product').all()
    serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','patch','post','delete']
    def get_queryset(self):
       return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk']) 
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    


class CustomerViewset(ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[IsAuthenticated]

    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        (customer,created_at)=Customer.objects.get_or_create(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
        
        
class OrderViewSet(ModelViewSet):
    http_method_names=[ 'post','patch','delete','head','get','options']
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            queryset = Order.objects.all()
            
        (customer_id,created_at)=Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CreateOrderSerializer
        elif self.request.method=='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
  
    def create(self, request, *args, **kwargs):
        serializer=CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order=serializer.save()
        serializer=OrderSerializer(order)
        return Response(serializer.data)



    
class ProductImageViewSet(ModelViewSet):
    serializer_class=ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['products_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['products_pk']}

    

    
    





