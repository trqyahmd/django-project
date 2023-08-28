from django.contrib import admin
from .models import Product, Category, ProductImage, Size, Cart, Comment, Blog, BlogImage, Contact

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, )

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    inlines = (BlogImageInline, )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(BlogImage)