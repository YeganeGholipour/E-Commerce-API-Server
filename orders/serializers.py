from rest_framework import serializers
from .models import Order, Shipping, DiscountCode, UserDiscountCode

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['delivery_date', 'delivery_method', 'address', 'cost']
        read_only_fields = ['cost']  

    @staticmethod
    def calculate_cost(delivery_method):
        """Determine shipping cost based on the chosen delivery method."""
        return 10.00 if delivery_method == 'Express' else 5.00  

    def save(self, **kwargs):
        """Set shipping cost before saving."""
        delivery_method = self.validated_data.get('delivery_method', 'Standard')
        self.validated_data['cost'] = self.calculate_cost(delivery_method)
        return super().save(**kwargs)


class OrderSerializer(serializers.ModelSerializer):
    shipping = ShippingSerializer(required=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['payment_method', 'discount_code', 'final_price', 'shipping']
        read_only_fields = ['cart', 'created_at', 'updated_at', 'payment_status', 'taxt']
    
    def validate_discount_code(self, value):
        try:
            discount_code = DiscountCode.objects.get(code=value)
        except DiscountCode.DoesNotExist:
            raise serializers.ValidationError("Invalid discount code.")

        if not discount_code.is_valid():
            raise serializers.ValidationError("Discount code is expired or invalid.")

        if UserDiscountCode.objects.filter(user=self.context['request'].user, discount_code=discount_code).exists():
            raise serializers.ValidationError("You have already used this discount code.")

        return discount_code

    def create(self, validated_data):
        shipping_data = validated_data.pop('shipping')
        shipping = Shipping.objects.create(**shipping_data)

        cart = self.context['request'].user.cart
        validated_data['cart'] = cart

        discount_code = validated_data.get('discount_code')
        if discount_code:
            UserDiscountCode.objects.create(user=self.context['request'].user, discount_code=discount_code)

        order = Order.objects.create(shipping=shipping, discount_code=discount_code, **validated_data)
        return order
    
    def update(self, instance, validated_data):
        shipping_data = validated_data.pop('shipping', None)

        if shipping_data:
            shipping = instance.shipping
            shipping.delivery_date = shipping_data.get('delivery_date', shipping.delivery_date)
            shipping.delivery_method = shipping_data.get('delivery_method', shipping.delivery_method)
            shipping.address = shipping_data.get('address', shipping.address)
            shipping.save()

        return super().update(instance, validated_data)
    
        # shipping_data = validated_data.pop('shipping', None)

        # if shipping_data:
        #     for attr, value in shipping_data.items():
        #         setattr(instance.shipping, attr, value)
        #     instance.shipping.save()

        # return super().update(instance, validated_data)

    
    