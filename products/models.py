from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/categories/{self.slug}/"
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    sku = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/products/{self.sku}/"
    
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def apply_discount(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.count() == 0:
            return 0
        return sum([review.rating for review in reviews]) / reviews.count()


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
    
    def approve(self):
        self.status = "approved"
        self.save()
    
    def reject(self):
        self.status = "rejected"
        self.save()
    
    def is_approved(self):
        return self.status == "approved"