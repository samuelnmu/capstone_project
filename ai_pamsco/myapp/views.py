# Django REST Framework imports
from rest_framework import viewsets, permissions

# Import Models & Serializers
from .models import CustomUser, Product, Order, MarketPrice
from .serializers import (
    CustomUserSerializer,
    ProductSerializer,
    OrderSerializer,
    MarketPriceSerializer,
)

# Django Authentication & Utility imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#       API VIEWSETS

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Custom Users.
    - Admins can view/create/delete all users.
    - Regular users can only view their own profile.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict non-admin users to their own profile only.
        """
        user = self.request.user
        if user.role == "admin":
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Products.
    - Farmers can create/update/delete their products.
    - All logged-in users can view products.
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Attach the logged-in farmer as the product owner.
        """
        serializer.save(farmer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Orders.
    - Buyers can create new orders.
    - Orders are tied to the logged-in buyer.
    """

    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Use serializer's create() method to handle order creation.
        """
        serializer.save()

    def get_queryset(self):
        """
        - Admins see all orders.
        - Buyers only see their own orders.
        """
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(buyer=user)


class MarketPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Market Prices.
    - Admins can add new prices.
    - All users can view prices.
    """

    queryset = MarketPrice.objects.all().order_by("-date_recorded")
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]


#       HTML VIEWS

def register_page(request):
    """
    Render the registration page (GET).
    """
    return render(request, "myapp/register.html")


def login_page(request):
    """
    Handle user login.
    - Accepts email & password.
    - Redirects user based on role after login.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate with email & password (requires AUTH_USER_MODEL setup)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Redirect user based on their role
            if user.role == "farmer":
                return redirect("farmer_home")
            elif user.role == "buyer":
                return redirect("buyer_home")
            elif user.role == "transporter":
                return redirect("transporter_home")
            else:
                return redirect("home")  # fallback for admin/others
        else:
            # Invalid credentials
            messages.error(request, "Invalid email or password")

    # If GET or login failed, show login page again
    return render(request, "myapp/login.html")


def logout_view(request):
    """
    Log out the user and redirect to login page.
    """
    auth_logout(request)
    return redirect("login")


@login_required
def home_page(request):
    """
    Home page after login (for general users).
    """
    return render(request, "myapp/homepage.html", {"user": request.user})


@login_required
def farmer_home(request):
    """
    Dashboard for Farmers.
    """
    return render(request, "myapp/farmer_home.html", {"user": request.user})


@login_required
def buyer_home(request):
    """
    Dashboard for Buyers.
    """
    return render(request, "myapp/buyer_home.html", {"user": request.user})


@login_required
def transporter_home(request):
    """
    Dashboard for Transporters.
    """
    return render(request, "myapp/transporter_home.html", {"user": request.user})
