from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from services.options import payment_status
from services.mixin import SlugMixin
from django.utils.text import slugify


User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    about_us = RichTextField(blank = True, null = True)
    activation_link = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, default="")  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username) 
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username
    

class Addresses(models.Model):
    address = models.ForeignKey(User, on_delete = models.CASCADE)
    telephone = PhoneNumberField(null = True, default = None)
    country = models.CharField(max_length = 200 ,blank = True, null = True, default= None)
    city = models.CharField(max_length = 200, blank= True, null = True, default = None)
    street = models.CharField(max_length = 200,blank = True, null = True, default = None)
    zip_code = models.CharField(max_length = 5, default = None)

    def __str__(self) -> str:
        return self.user.address
    

# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete = models.CASCADE)
#     status = models.CharField(max_length = 20, choices = payment_status)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self) -> str:
#         return f"{self.amount} ({self.status}) on {self.payment_date}"


