from django.db import models
from ckeditor.fields import RichTextField
from services.mixin import DateMixin, SlugMixin
from mptt.models import TreeForeignKey, MPTTModel
from services.generator import CodeGenerator, ProductCodeGenerator
from services.slugify import slugify
from services.options import product_status, clothing_size, color
from services.uploader import Uploader
import uuid
from django.contrib.auth import get_user_model
from django.db.models import Q, F


User = get_user_model()

class Category(DateMixin, SlugMixin, MPTTModel):
    name = models.CharField(max_length=300)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null = True, blank = True, related_name = 'children')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size = 20, model_ = Category
        )
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    @property
    def product_count(self):
        return Product.objects.filter(
            Q(category_id=self.id)|Q(category__parent_id=self.id)|
            Q(category__parent__parent_id=self.id)
        ).count()
    
class Size(models.Model):
    name = models.CharField(max_length=200, choices = clothing_size)

    def __str__(self) -> str:
        return self.name

class Product(DateMixin, SlugMixin):
    name = models.CharField(max_length = 200)
    description = RichTextField(blank = True, null = True)
    price = models.FloatField()
    discount = models.FloatField(blank = True, null = True)
    status = models.CharField(max_length=200, choices = product_status)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    size = models.ManyToManyField(Size)
    weight = models.FloatField(blank = True, null = True)
    color = models.CharField(max_length = 200, choices = color)
    product_code = models.CharField(max_length = 50, unique = True, editable = False)
    wishlist = models.ManyToManyField(User, blank = True)
    composition = models.TextField(blank=True, null=True)
    

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_code = ProductCodeGenerator.create_product_code(size=8, model_=Product)
            self.slug = slugify(self.name)
            self.code = CodeGenerator.create_slug_shortcode(size = 20, model_ = Product)
        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     self.code = ProductCodeGenerator.create_product_code(
    #         size = 8, model_ = Product
    #     )
    
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    # def save(self, *args, **kwargs):
    #     self.code = CodeGenerator.create_slug_shortcode(
    #         size = 20, model_ = Product
    #     )
    #     self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

class StockStatus(models.Model):
    status_stock = models.CharField(max_length=20, unique=True)
        
    

class ProductImage(DateMixin):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = Uploader.upload_image_product)

    def __str__(self) -> str:
        return self.product.name
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'


        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}  --  {self.product.name}" 
    


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name = 'comments', on_delete = models.CASCADE)
    commenter_name = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_body = RichTextField()
    rate = models.IntegerField(default = 0)
    published_date = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return '%s - %s' % (self.product.name, self.commenter_name)

class Blog(models.Model):
    head = models.CharField(max_length=200)
    time = models.DateTimeField(blank=True, null=True)
    desc = RichTextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.head

class BlogImage(DateMixin):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = Uploader.upload_image_blog)

    def __str__(self) -> str:
        return self.blog.head
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Blog Gallery'
        verbose_name_plural = 'Blog Galleries'


class Contact(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.subject