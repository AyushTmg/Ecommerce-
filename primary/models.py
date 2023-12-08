from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin
from .validators import validate_file_size
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name="+")

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['id']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug=models.SlugField()
    description = models.TextField(null=True,blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    
    promotions = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']

class ProductImage(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='image')
    image=models.ImageField(upload_to='primary/images')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.first_name
    
    class Meta:
        ordering=['user__first_name','user__last_name']
        permissions=[
            ('view_history','Can view history')
        ]

    @admin.display(ordering='user_first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user_last_name')
    def last_name(self):
        return self.user.last_name
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)
    description=models.TextField()
    date=models.DateField(auto_now_add=True)



class Order(models.Model):
    PENDING="P"
    COMPLETE='C'
    FAILED='F'
    PAYMENT_STATUS=[
        (PENDING,"Pending"),
        (COMPLETE,"Complete"),
        (FAILED,"Failed")
    ]
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='order')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='orderitem')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,validators=[MinValueValidator(1)])


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together=(('cart','product'),)


