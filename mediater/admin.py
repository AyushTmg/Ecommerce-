from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem
from primary.admin import ProductAdmin,ProductImageInline
from primary.models import Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
        search_fields=['first_name__icontains']
        add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name","last_name","email","username", "password1", "password2"),
            },
        ),
    )



class TagInline(GenericTabularInline):
    autocomplete_fields=['tag']
    model=TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines=[TagInline,ProductImageInline]

admin.site.unregister(Product)

admin.site.register(Product,CustomProductAdmin)
   

