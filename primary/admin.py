from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Product,Collection,Order,Customer,OrderItem,ProductImage
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display =['id','title','product_count']
    search_fields=['title']
    autocomplete_fields=['featured_product']

    @admin.display(ordering='product_count')
    def product_count(self,collection:Collection):
        url=reverse('admin:primary_product_changelist')+'?'+urlencode({'collection_id':str(collection.id)})

        return format_html('<a href="{}" target="_blank">{}</a>',url,collection.product_count)
    

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(product_count=Count('product'))


class InventoryFilter(admin.SimpleListFilter):
    title="Inventory Status"
    parameter_name='On the basis of inventory'

    def lookups(self, request: Any, model_admin: Any):
        return [
            ('<50','Low'),
            ('>50','High')
        ]
    
    def queryset(self, request, queryset: QuerySet) :
        if self.value()=='<50':
            return queryset.filter(inventory__lt=50)
        if self.value()=='>50':
            return queryset.filter(inventory__gt=50)

class ProductImageInline(admin.TabularInline):
    model=ProductImage
    readonly_fields=['thumbnail']

    def thumbnail(self,instance):
        if instance.image.name!='':
            return format_html(f"<img src='{instance.image.url}' class='thumbnail'/>")                     
        return ""
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    fields=['title','slug','description','unit_price','inventory','promotions']
    prepopulated_fields={
        'slug':['title']
    }
    readonly_fields=['promotions']
    list_display = ['title','unit_price','inventory','collection','inventory_status']
    list_editable=['unit_price']
    list_per_page=10
    list_filter=['collection',InventoryFilter]
    search_fields=['title__istartswith']
    actions=['clear_inventory','add_inventory']
    autocomplete_fields=['collection']



    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset:QuerySet):
        update_count=queryset.update(inventory=0)
        return self.message_user(request,f"{update_count} has been successfully updated")



    @admin.action(description='Add_inventory')
    def add_inventory(self,request,queryset:QuerySet):
        update_count=queryset.update(inventory=100)
        return self.message_user(request,f"{update_count} has been successfully updated")
    

    @admin.display(ordering='inventory')
    def inventory_status(self,product:Product):
        if product.inventory<50:
            return "Lt50"
        return 'Gt50'

    class Media:
        css={
            'all':['style.css']
        }
        
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','phone','full_order']
    list_editable=['phone']
    list_per_page=10
    list_select_related=['user']
    search_fields=['user__first_name__istartswith']
    autocomplete_fields=['user']

    @admin.display(ordering='full_order')
    def full_order(self,customer:Customer):
        url=reverse('admin:primary_order_changelist')+'?'+urlencode({'customer_id':str(customer.id)})

        return format_html('<a href="{}" target="_blank">{}</a>',url,customer.full_order)
    

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(full_order=Count('order'))
    
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    autocomplete_fields=['product']
    extra=3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    list_display=['fullname','placed_at','payment_status']
    list_editable=['payment_status']
    list_per_page=10
    list_select_related=['customer']
    autocomplete_fields=['customer']
    

    def fullname(self,order:Order):
        return order.customer.first_name+" "+order.customer.last_name



