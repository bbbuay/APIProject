from rest_framework import serializers
from .models import MenuItem, Cart, Order
from django.contrib.auth.models import User

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ["title", "price", "featured", "category", "category_id"]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ["id", "username", "first_name", "last_name", "email"]

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    delivery_crew = serializers.StringRelatedField(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = "__all__"

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]



