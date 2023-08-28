from django.db.models.functions import Coalesce
from django.db.models import FloatField, F, Case, When
from products.models import Product

def get_products_with_discount():
    return Product.objects.annotate(
        discount_percent=Coalesce(F('discount'), 0, output_field=FloatField())
    ).annotate(
        total_price=Case(
            When(discount_percent=0, then=F('price')),
            default=F('price') - (F('price') * F('discount_percent') / 100),
            output_field=FloatField()
        )
    ).order_by('-created_at')