from django.urls import path
from rest_framework.routers import DefaultRouter

from shop import views

app_name = 'shop'

router = DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
router.register("product", views.ProductViewSet, basename="product")
router.register("cart", views.CartViewSet, basename="cart")
router.register("cart-item", views.CartItemViewSet, basename="cart-item")

urlpatterns = [
    path('update-cart-item/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('get-cart-items-list/', views.CartView.as_view(), name= "get-cart-items-list"),

              ] + router.urls
