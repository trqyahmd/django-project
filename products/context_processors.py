from .models import Product, Cart

def product_count_context(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(wishlist__in=[request.user])
        product_count = products.count()
    else:
        product_count = 0

    return {
        'global_product_count': product_count,
    }

def cart_products_count(request):
    if request.user.is_authenticated:
        from .models import Cart  
        carts = Cart.objects.filter(user=request.user)
        products_count = carts.count()
    else:
        products_count = 0

    return {
        'global_products_count': products_count,
    }