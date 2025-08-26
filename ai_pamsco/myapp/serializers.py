from rest_framework import serializers
from .models import CustomUser, Product, Order, MarketPrice
from .sanitizers import sanitize_text


# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializes CustomUser model.
    Handles validation and sanitization of user data.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "location"]

    def validate_email(self, value):
        """Ensure email is lowercase and unique."""
        email = value.lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return email

    def validate_location(self, value):
        """Sanitize and validate location field."""
        return sanitize_text(value)


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    farmer = serializers.ReadOnlyField(source="farmer.username")  # Show farmer username instead of ID

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "quantity", "category",
                  "image_url", "farmer", "location", "created_at"]

    def validate_name(self, value):
        """Sanitize product name."""
        return sanitize_text(value)

    def validate_quantity(self, value):
        """Ensure product quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_price(self, value):
        """Ensure product price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source="buyer.username")
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = Order
        fields = [
            "id", "buyer", "product", "product_name", "quantity", "total_price",
            "payment_status", "order_status", "created_at"
        ]
        read_only_fields = ["total_price", "buyer", "product_name"]

    def create(self, validated_data):
        request = self.context["request"]
        buyer = request.user
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        total_price = product.price * quantity

        return Order.objects.create(
            buyer=buyer,
            total_price=total_price,
            **validated_data
        )


# Market Price Serializer
class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = ["id", "product_name", "region", "price", "date_recorded"]

    def validate_product_name(self, value):
        """Sanitize product name."""
        return sanitize_text(value)

    def validate_price(self, value):
        """Ensure market price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
