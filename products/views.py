from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Comment, Category, Blog, Size
from django.db.models.functions import Coalesce
from django.db.models import FloatField, F, Case, When, Q, Sum, Count
from django.http import JsonResponse
from products.models import Cart
from .product_utils import get_products_with_discount
from .forms import CommentForm, ProductSearchForm, ContatForm
import datetime
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

def home_view(request):

    query = request.GET.get('q')
    if query is None:
        query = ""

    products = Product.objects.annotate(
        discount_percent = Coalesce(F('discount'), 0, output_field = FloatField())
    ).annotate(
        total_price = Case(
            When(discount_percent = 0, then = F('price')),
            default = F('price') - (F('price') * F('discount_percent') / 100),
            output_field = FloatField() 
        )
    ).order_by('-created_at')

    comments = Comment.objects.all()
    blogs = Blog.objects.all()[::3]

    if query:
        products = products.filter(Q(name__icontains=query)|Q(product_code=query))

    context = {
        'products' : products,
        'search_query': query,
        'comments': comments,
        'blogs': blogs,
    }
    
    return render(request, 'products/home.html', context)


def product_search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(product_code__icontains = q)
        context = {
            'products' : products,
            'query' : q
        }

    else:
        context = {

        }

    return render(request, 'products/home.html', context)

# def product_detail_view(request, id):

#     product = get_object_or_404(Product, id = id)

#     products = Product.objects.annotate(
#         discount_percent = Coalesce(F('discount'), 0, output_field = FloatField())
#     ).annotate(
#         total_price = Case(
#             When(discount_percent = 0, then = F('price')),
#             default = F('price') - (F('price') * F('discount_percent') / 100),
#             output_field = FloatField() 
#         )
#     ).order_by('-created_at')

#     num_comments = Comment.objects.filter(product=product).count()

#     context = {
#         'product' : product,
#         'products': products,
#         'num_comments': num_comments,
#     }

#     return render(request, 'products/detail.html', context)

@login_required
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)

    # Calculate total_price only for the current product
    total_price = product.price
    if product.discount:
        total_price = product.price - (product.price * product.discount / 100)

    
    products = Product.objects.annotate(
        discount_percent = Coalesce(F('discount'), 0, output_field = FloatField())
    ).annotate(
        total_price = Case(
            When(discount_percent = 0, then = F('price')),
            default = F('price') - (F('price') * F('discount_percent') / 100),
            output_field = FloatField() 
        )
    ).order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.commenter_name = request.user
            new_comment.save()
            return redirect('products:detail', id=id)
    else:
        comment_form = CommentForm()




    context = {
        'product': product,
        'total_price': total_price,
        'comment_form': comment_form,
        'products': products,
    }

    return render(request, 'products/detail.html', context)



# def product_detail_view(request, id):
#     search_form = ProductSearchForm(request.GET or None)
#     product = None

#     if search_form.is_valid():
#         search_query = search_form.cleaned_data['search_query']
#         try:
#             product = Product.objects.get(product_code=search_query)
#         except Product.DoesNotExist:
#             product = None
#     else:
#         product = get_object_or_404(Product, id=id)

#     if product:
#         discount_percent = product.discount or 0
#         total_price = product.price - (product.price * discount_percent / 100)

#         num_comments = Comment.objects.filter(product=product).count()

#         context = {
#             'product': product,
#             'total_price': total_price,
#             'num_comments': num_comments,
#             'search_form': search_form,
#         }

#         return render(request, 'products/detail.html', context)
#     else:
#         return render(request, 'products/product_not_found.html')


@login_required
def product_wishlist_view(request):

    data = {}

    product = get_object_or_404(Product, id = int(request.POST.get("id")))

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
        data["success"] = False

    else:
        product.wishlist.add(request.user)
        data["success"] = True
    return JsonResponse(data)

def product_cart_view(request):

    data = {}

    product = get_object_or_404(Product, id = int(request.POST.get("id")))

    Cart.objects.get_or_create(
        product = product,
        user = request.user
    )
    
    return JsonResponse(data)

# @login_required
# def wishlist_view(request):
#     products = Product.objects.annotate(
#         discount_percent = Coalesce(F('discount'), 0, output_field = FloatField())
#     ).annotate(
#         total_price = Case(
#             When(discount_percent = 0, then = F('price')),
#             default = F('price') - (F('price') * F('discount_percent') / 100),
#             output_field = FloatField() 
#         )
#     ).filter(
#         wishlist__in = [request.user]
#     )

    
#     context = {
#         'products' : products,
#     }

#     return render(request, 'products/wishlist.html', context)

@login_required
def wishlist_view(request):
    products = Product.objects.annotate(
        discount_percent=Coalesce(F('discount'), 0, output_field=FloatField())
    ).annotate(
        total_price=Case(
            When(discount_percent=0, then=F('price')),
            default=F('price') - (F('price') * F('discount_percent') / 100),
            output_field=FloatField()
        )
    ).filter(
        wishlist__in=[request.user]
    )

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,  
    }

    return render(request, 'products/wishlist.html', context)

# @login_required()
# def cart_list_view(request):
#     carts = Cart.objects.annotate(
#         product_total_price = Case(
#             When(product__discount__isnull = True, then = F('product__price')),
#             default = F("product__price") - F("product__discount"),
#             output_field = FloatField()
#         )
#     ).filter(user = request.user)

#     total_sum = carts.aggregate(total_sum=Sum('product_total_price'))['total_sum'] or 0

#     sep_prices = [cart.product_total_price for cart in carts]

#     applied_coupon = request.session.get('applied_coupon', '')

#     products_count = carts.count()

#     context = {
#         "carts": carts,
#         'total_sum': total_sum,
#         'sep_prices': sep_prices,
#         'applied_coupon': applied_coupon,
#         'products_count': products_count,
#     }

#     return render(request, 'products/shopping-cart.html', context)

@login_required
def cart_list_view(request):
    carts = Cart.objects.annotate(
        product_total_price=Case(
            When(product__discount__isnull=True, then=F('product__price')),
            default=F("product__price") - F("product__discount"),
            output_field=FloatField()
        )
    ).filter(user=request.user)

    total_sum_dict = carts.aggregate(total_sum=Sum('product_total_price'))
    total_sum = total_sum_dict['total_sum'] if total_sum_dict['total_sum'] is not None else 0

    sep_prices = [cart.product_total_price for cart in carts]

    applied_coupon = request.session.get('applied_coupon', '')

    products_count = carts.count()

    context = {
        "carts": carts,
        'total_sum': total_sum,
        'sep_prices': sep_prices,
        'applied_coupon': applied_coupon,
        'products_count': products_count,
    }

    return render(request, 'products/shopping-cart.html', context)



# def add_comment(request, id):
#     product = Product.objects.get(id = id)

#     form = CommentForm(instance = product)

#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance = product)
#         if form.is_valid():
#             name= request.user.username
#             body = form.cleaned_data['comment_body'];
#             c = Comment(product = product, commenter_name = name, comment_body = body, published_date = datetime.now())
#             c.save()
#         else:
#             print('Formu düzgün doldurun!') 

#     else:
#         form = CommentForm()

#     context = {
#         'form': form,
#     }

#     return render(request, 'products/detail.html', context)

def add_comment(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(product=product, commenter_name=name, comment_body=body, published_date=datetime.now())
            c.save()
        else:
            print('Formu düzgün doldurun!')
    else:
        form = CommentForm()

    context = {
        'form': form,
        'product': product,  
    }

    return render(request, 'products/detail.html', context)


def delete_comment(request, id):
    comment = Comment.objects.filter(product = id)
    comment.delete()
    return redirect('products:home')


def shop_list_view(request):

    query = request.GET.get('q')
    if query is None:
        query = ''

    filter_, filter_dict = Q(), {}

    products = Product.objects.annotate(
        discount_percent = Coalesce(F('discount'), 0, output_field = FloatField())
    ).annotate(
        total_price = Case(
            When(discount_percent = 0, then = F('price')),
            default = F('price') - (F('price') * F('discount_percent') / 100),
            output_field = FloatField() 
        )
    ).order_by('-created_at')

    if query:
        products = products.filter(Q(name__icontains=query)|Q(product_code=query))

    # category = request.GET.getlist('category',None)
    # if category:
    #     products = products.filter(
    #         category__parent__parent_id__in=category
    #     )

    sort_option = request.GET.get('sort')
    category = request.GET.getlist('category',None)
    color = request.GET.get('color',None)
    size = request.GET.getlist('size', None)
    my_price = request.GET.get('my-price', None)

    if sort_option == "low_price":
        products = products.order_by('total_price')
    elif sort_option == "high_price":
        products = products.order_by('-total_price')

    if category:
        filter_.add(Q(category__parent__parent_id__in=category)|Q(category__parent_id__in=category)|Q(category_id__in=category), Q.AND)

        filter_dict["category"] = f"category={category}&"

        # products = products.filter()
    if color:
        filter_.add(Q(color=color), Q.AND)

    if size:
        filter_.add(Q(size__in=size), Q.AND)

    if my_price:
        my_price = my_price.split(';')
        min_price = my_price[0]
        max_price = my_price[1]
        filter_.add(Q(total_price__gte=min_price),Q.AND)
        filter_.add(Q(total_price__lte=max_price),Q.AND)

    products = products.filter(filter_)

    # print(request.GET.get('my-price'))
    

    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)
    product_list = paginator.get_page(page)




    context = {
        'categories': Category.objects.filter(parent__isnull=True).order_by('-created_at'),
        'products': product_list,
        'paginator': paginator,
        'size_list': Size.objects.all,
        'search_query': query,

    }


    return render(request, 'products/shop-list.html',context)


def bloggs(request):
    blogs = Blog.objects.all()

    paginator = Paginator(blogs, 4)
    page = request.GET.get('page', 1)
    blog_list = paginator.get_page(page)

    context = {
        'blogs': blogs,
        'products': blog_list,
        'paginator': paginator,
    }

    return render(request, 'products/blog.html', context)

# def blog_detail_view(request, id):

#     blog = get_object_or_404(Blog, id = id)

#     blogs = Blog.objects.all()


#     context = {
#         'blog' : blog,
#         'blogs': blogs,
#     }

#     return render(request, 'products/detail.html', context)

def about_us_view(request):

    context = {

    }

    return render(request,'products/about-us.html',context)

def privacy(request):

    context = {

    }

    return(request, 'products/privacy.html', context)

def contact(request):

    context = {

    }

    return render(request, 'products/contact.html', context)

def faq(request):

    context = {

    }

    return render(request, 'products/faq.html', context)


def checkout_view(request):

    carts = Cart.objects.annotate(
        product_total_price = Case(
            When(product__discount__isnull = True, then = F('product__price')),
            default = F("product__price") - F("product__discount"),
            output_field = FloatField()
        )
    ).filter(user = request.user)

    total_sum = carts.aggregate(total_sum=Sum('product_total_price'))['total_sum'] or 0

    sep_prices = [cart.product_total_price for cart in carts]

    applied_coupon = request.session.get('applied_coupon', '')

    products_count = carts.count()

    context = {
        "carts": carts,
        'total_sum': total_sum,
        'sep_prices': sep_prices,
        'applied_coupon': applied_coupon,
        'products_count': products_count,
    }

    return render(request, 'products/checkout.html',context)

def ordercomplete_view(request):

    context = {

    }

    return render(request, 'products/complete-order.html', context)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
    return redirect(reverse('products:detail', args=[comment.product.id]))  

def wishlist_delete(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        if request.user in product.wishlist.all():
            product.wishlist.remove(request.user)
    return redirect('products:products-in-wishlist')

def wishlist_clean(request):
    if request.method == 'POST':
        request.user.product_set.clear()
    return redirect('products:products-in-wishlist')

def cart_list_clean(request):
    if request.method == 'POST':
        Cart.objects.filter(user=request.user).delete()
    return redirect('products:shopping-cart-list')


VALID_COUPON_CODES = ['KUMO123', 'KUMO50%', 'SUMMERHOLIDAY']

# def apply_coupon(request):
#     coupon_code = request.POST.get('coupon_code')
#     print("Entered Coupon Code:", coupon_code)

#     if request.method == 'POST':

#         if coupon_code in VALID_COUPON_CODES: 
#             request.session['applied_coupon'] = coupon_code
#             request.session.modified = True
#             total_sum *= 0.5  
#     carts = Cart.objects.filter(user=request.user)
#     total_sum = sum(cart.product_total_price for cart in carts)

#     return redirect('products:shopping-cart-list')

# def apply_coupon(request):
#     if request.method == 'POST':
#         coupon_code = request.POST.get('coupon_code')
#         print("Entered Coupon Code:", coupon_code)

#         if coupon_code in VALID_COUPON_CODES:
#             request.session['applied_coupon'] = coupon_code
#             request.session.modified = True

#             carts = Cart.objects.filter(user=request.user)
#             total_sum = sum(cart.product_total_price for cart in carts)
#             total_sum *= 0.5  # Apply the 50% discount

#             return redirect('products:shopping-cart-list')

#     return redirect('products:shopping-cart-list') 

# def apply_coupon(request):
#     if request.method == 'POST':
#         coupon_code = request.POST.get('coupon_code')
#         print("Entered Coupon Code:", coupon_code)

#         if coupon_code in VALID_COUPON_CODES:
#             request.session['applied_coupon'] = coupon_code
#             request.session.modified = True

#             carts = Cart.objects.annotate(
#                 product_total_price=Case(
#                     When(product__discount__isnull=True, then=F('product__price')),
#                     default=F("product__price") - F("product__discount"),
#                     output_field=FloatField()
#                 )
#             ).filter(user=request.user)
            
#             total_sum = sum(cart.product_total_price for cart in carts)
#             discounted_total_sum = total_sum * 0.5  
#             sep_prices = [cart.product_total_price for cart in carts]
#             applied_coupon = request.session.get('applied_coupon', '')

#             context = {

#                 'applied_coupon': applied_coupon,
#                 'total_sum': total_sum,
#                 'sep_prices': sep_prices,
#                 'carts': carts,
#                 'discounted_total_sum': discounted_total_sum,
#             }

#             # return redirect('products:shopping-cart-list')

#             return render(request, 'products/shopping-cart.html', context)

#     return redirect('products:shopping-cart-list') 

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        print("Entered Coupon Code:", coupon_code)

        if coupon_code in VALID_COUPON_CODES:
            request.session['applied_coupon'] = coupon_code
            request.session.modified = True

            carts = Cart.objects.annotate(
                product_total_price=Case(
                    When(product__discount__isnull=True, then=F('product__price')),
                    default=F("product__price") - F("product__discount"),
                    output_field=FloatField()
                )
            ).filter(user=request.user)
            
            total_sum = sum(cart.product_total_price for cart in carts)
            discounted_total_sum = total_sum * 0.5

            sep_prices = [cart.product_total_price for cart in carts]
            applied_coupon = coupon_code  # Pass the coupon code directly

            context = {
                'total_sum': total_sum,
                'sep_prices': sep_prices,
                'carts': carts,
                'discounted_total_sum': discounted_total_sum,
            }

            messages.success(request, f"Kupon kodu: '{applied_coupon}' uğurla tətbiq edildi!")

            return render(request, 'products/shopping-cart.html', context)
        else:
            messages.error(request, "Keçərsiz kupon kodu!")

    return redirect('products:shopping-cart-list')


def contact_view(request):
    form = ContatForm()
    if request.method == 'POST':
        form = ContatForm(request.POST)
        description = request.POST.get("description")
        if form.is_valid():
            form.save(commit=False)
            form.description=description
            form.save()

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['description']
            sender_email = ['email']
            recipient_list = [settings.CONTACT_EMAIL]

            # send_mail(
            #     subject,
            #     message,
            #     sender_email,
            #     recipient_list
            # )

            return redirect('products:home')

    else:
        form = ContatForm()

    context = {
        'form': form,
    }

    return render(request,'products/contact.html', context)