from rest_framework import serializers
from .models import Product, Category, Review

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__" 
        extra_kwargs = {"average_rating": {"read_only": True}}

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_is_in_stock(self, obj):
        return obj.is_in_stock()

    def get_final_price(self, obj):
        return obj.apply_discount()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]