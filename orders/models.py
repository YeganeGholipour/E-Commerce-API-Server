from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from cart.models import Cart
from django.utils import timezone

user = get_user_model()

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1, help_text="How many times a user can use this code")

    def is_valid(self):
        total_usage = Order.objects.filter(discount_code=self).count()
        return (
            self.valid_from <= timezone.now() <= self.valid_to
            and total_usage < self.usage_limit
        )
    
    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class UserDiscountCode(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'discount_code')

    def __str__(self):
        return f"{self.user.username} used {self.discount_code.code}"



class Shipping(models.Model):
    DELIVERY_METHOD_CHOICES = (
        ('Standard', 'Standard'),
        ('Express', 'Express')
    )

    DELIVERY_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )

    delivery_date = models.DateField()
    delivery_method = models.CharField(choices=DELIVERY_METHOD_CHOICES, max_length=10, default='Standard')
    delivery_status = models.CharField(choices=DELIVERY_STATUS_CHOICES, max_length=10, default='Pending')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()

    def clean(self):
        """Ensure delivery date is not in the past"""
        if self.delivery_date < timezone.now().date():
            raise ValidationError("Delivery date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delivery_method} - {self.cost} USD"


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled')
    )

    PAYMENT_METHOD_CHOICES = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment')
    )

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, max_length=10, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, max_length=20, default='Cash on Delivery')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    shipping = models.OneToOneField(Shipping, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order #{self.id} - {self.cart.user.username}"

    def final_price(self):
        total_price = self.cart.total_price()  
        shipping_cost = self.shipping.cost if self.shipping else 0

        if self.discount_code and self.discount_code.is_valid():
            discount_amount = (total_price * self.discount_code.discount_percent) / 100
            total_price -= discount_amount

        return total_price + shipping_cost