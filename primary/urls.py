from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewset,basename='customer')
router.register('orders',views.OrderViewSet,basename='orders')

product_router=routers.NestedDefaultRouter(router,'products',lookup='products')
product_router.register('reviews',views.ReviewViewSet,basename='product_review')
product_router.register('images',views.ProductImageViewSet,basename='product_image')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart_items')

urlpatterns = router.urls+product_router.urls +cart_router.urls
