# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ProductViewSet, OrderViewSet, MarketPriceViewSet, register_page, login_page

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'market-prices', MarketPriceViewSet, basename='marketprice')

# The API URLs are now determined automatically by the router
# App-level urlpatterns
urlpatterns = [
    # HTML page
    path("register/", register_page, name="register"),
    path("login/", login_page, name="login"),


    # API endpoints
    path("api/", include(router.urls)),
]