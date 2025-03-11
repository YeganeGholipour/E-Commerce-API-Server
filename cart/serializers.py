from rest_framework import serializers
from .models import CartItem, Cart

class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["product", "quantity", "price", "cart"]
        read_only_fields = ["cart"]  

    def create(self, validated_data):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)  
        return super().create({**validated_data, "cart": cart})  

    def get_price(self, obj):
        return obj.price()

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True, source="items")  

    class Meta:
        model = Cart
        fields = ["id", "updated_at", "created_at", "cart_items"] 
        read_only_fields = ["updated_at", "created_at"]
