from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product

class User(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    phone_number = models.CharField(max_length=11, blank=False, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True, blank=True)

    def update_email(self, new_email):
        if User.objects.filter(email=new_email).exists():
            raise ValueError("Email already exists")
        self.email = new_email
        self.save()
    
    def update_phone_number(self, new_phone_number):
        if len(new_phone_number) < 11:
            raise ValueError("Invalid phone number")
        self.phone_number = new_phone_number
        self.save()
    
    def update_date_of_birth(self, new_date_of_birth):
        self.date_of_birth = new_date_of_birth
        self.save()
    
    def update_gender(self, new_gender):
        self.gender = new_gender
        self.save()


class WishList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    