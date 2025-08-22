from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Order, MarketPrice

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Allows managing users with roles (farmer, buyer, transporter, admin).
    """

    model = CustomUser

    # Fields displayed in the list view of users
    list_display = ("username", "email", "role", "location", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")  # Filters sidebar
    search_fields = ("email", "username")            # Search bar fields
    ordering = ("email",)                            # Default ordering by email

    # Fields displayed when editing a user
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("role", "location")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    # Fields displayed when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "location", "password1", "password2", "is_staff", "is_active"),
        }),
    )


# Product Admin
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    Displays products with quick filtering and search.
    """
    list_display = ("name", "category", "price", "quantity", "farmer", "location", "created_at")
    list_filter = ("category", "location")  # Sidebar filters
    search_fields = ("name", "farmer__username")  # Search by product name or farmer username


# Order Admin
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Helps track order status and payment.
    """
    list_display = ("id", "buyer", "product", "quantity", "total_price", "payment_status", "order_status", "created_at")
    list_filter = ("payment_status", "order_status")  # Filter orders by status
    search_fields = ("buyer__username", "product__name")  # Search by buyer or product


# MarketPrice Admin
class MarketPriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for MarketPrice model.
    Useful for analyzing historical price data.
    """
    list_display = ("product_name", "region", "price", "date_recorded")
    list_filter = ("region",)  # Filter by region
    search_fields = ("product_name",)  # Search by product name


# Register models to admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MarketPrice, MarketPriceAdmin)

#admin(fintechsam_254)