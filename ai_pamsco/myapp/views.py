from rest_framework import viewsets, permissions
from .models import CustomUser, Product, Order, MarketPrice
from .serializers import (
    CustomUserSerializer,
    ProductSerializer,
    OrderSerializer,
    MarketPriceSerializer,
)
from django.shortcuts import render

# Handles CRUD operations for Users, Products, Orders, and Market Prices

# Custom User ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    - Only Admins can view/create/delete users.
    - Regular users can view their own profile.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict regular users to only their profile.
        Admins can see all users.
        """
        user = self.request.user
        if user.role == "admin":
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    - Farmers can create/update/delete their products.
    - All users can view products.
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Attach the logged-in farmer as product owner."""
        serializer.save(farmer=self.request.user)


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders.
    - Buyers can place new orders.
    - Orders are tied to the logged-in buyer.
    """
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Creation logic is handled in OrderSerializer.create()
        Just call save() with no extra args.
        """
        serializer.save()

    def get_queryset(self):
        """
        Buyers see their own orders.
        Admins can see all orders.
        """
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(buyer=user)

# Market Price ViewSet
class MarketPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for market prices.
    - Admins can add records.
    - All users can view market prices.
    """

    queryset = MarketPrice.objects.all().order_by("-date_recorded")
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]


# HTML

def register_page(request):
    return render(request, "myapp/register.html")

def login_page(request):
    return render(request, "myapp/login.html")
