# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ProductViewSet, OrderViewSet, MarketPriceViewSet, register_page, login_page, logout_view, home_page, login_page, farmer_home,buyer_home,transporter_home

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
    path("logout/", logout_view, name="logout"),
    path("home/", home_page, name="home"),
    path("login/", login_page, name="login"),
    
    path("farmer/home/", farmer_home, name="farmer_home"),
    path("buyer/home/", buyer_home, name="buyer_home"),
    path("transporter/home/", transporter_home, name="transporter_home"),
    # API endpoints for the router viewsets
    path("api/", include(router.urls)),
]