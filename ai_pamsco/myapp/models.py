from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# Custom User Manager
class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation.
    Provides methods to create both regular users and superusers.
    """

    def create_user(self, username, email, role, location, password=None):
        """
        Create and return a regular user with given details.
        - username: unique identifier for the user
        - email: user email (used as login field)
        - role: farmer, buyer, transporter, or admin
        - location: user’s location (e.g., Nairobi)
        - password: encrypted via set_password()
        """
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)  # Normalize email to lowercase
        user = self.model(
            username=username,
            email=email,
            role=role,
            location=location
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, role="admin", location="HQ", password=None):
        """
        Create and return a superuser.
        Superusers have all permissions and access to Django admin.
        """
        user = self.create_user(username, email, role, location, password)
        user.is_superuser = True   # Grants all permissions
        user.is_staff = True       # Allows access to Django admin
        user.save(using=self._db)
        return user


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for role-based authentication.
    Roles include Farmer, Buyer, Transporter, and Admin.
    """

    ROLE_CHOICES = (
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
        ("transporter", "Transporter"),
        ("admin", "Admin"),
    )

    username = models.CharField(max_length=50, unique=True)  # Unique username
    email = models.EmailField(unique=True)                   # Used for login
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # Defines user role
    location = models.CharField(max_length=100)              # User’s physical location

    # Default Django flags
    is_active = models.BooleanField(default=True)   # User can log in if active
    is_staff = models.BooleanField(default=False)   # True → Can access Django admin

    objects = CustomUserManager()  # Attach custom user manager

    # Django authentication settings
    USERNAME_FIELD = "email"   # Use email instead of username for login
    REQUIRED_FIELDS = ["username", "role", "location"]  # Required when creating superuser

    def __str__(self):
        return f"{self.username} ({self.role})"


# Product Model
class Product(models.Model):
    """
    Represents a product listed by a farmer.
    Each product is linked to a farmer (CustomUser with role=farmer).
    """

    CATEGORY_CHOICES = (
        ("grains", "Grains"),
        ("fruits", "Fruits"),
        ("vegetables", "Vegetables"),
        ("livestock", "Livestock"),
    )

    name = models.CharField(max_length=100)  # Product name (e.g., Maize)
    description = models.TextField(blank=True)  # Optional product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    quantity = models.PositiveIntegerField()  # Available quantity
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Product category
    image_url = models.URLField(blank=True, null=True)  # Optional image link
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )  # Farmer who owns the product
    location = models.CharField(max_length=100)  # Where the product is located
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.name} ({self.quantity})"


# Order Model
class Order(models.Model):
    """
    Represents an order placed by a buyer.
    Each order links a buyer → product → payment & status.
    """

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
    )
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )  # Buyer who places the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ordered product
    quantity = models.PositiveIntegerField()  # Quantity ordered
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Computed price
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")  # M-Pesa status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")  # Delivery status
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"


# Market Price Model
class MarketPrice(models.Model):
    """
    Tracks historical market price data for agricultural products.
    Useful for price analysis, charts, and AI predictions.
    """

    product_name = models.CharField(max_length=100)  # Name of product (e.g., Maize)
    region = models.CharField(max_length=100)        # Region of market data
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Recorded price
    date_recorded = models.DateField()  # Date of record

    def __str__(self):
        return f"{self.product_name} - {self.region} ({self.date_recorded})"
