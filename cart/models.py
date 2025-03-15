from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

user = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        total = sum(item.price() for item in self.items.all())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def price(self):
        price = self.product.apply_discount()
        return price * self.quantity

    def __str__(self):
        return f"{self.product.name} (Quantity: {self.quantity})"

    class Meta:
        unique_together = {"cart", "product"}
