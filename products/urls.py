from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [

    path('home/', views.home_view, name = 'home'),
    path('detail/<int:id>/', views.product_detail_view, name = 'detail'),
    # path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('wishlist/', views.product_wishlist_view, name = 'wishlist'),
    path('cart/', views.product_cart_view, name = 'cart'),
    path('products-in-wishlist/', views.wishlist_view, name = 'products-in-wishlist'),
    path('shopping-cart-list/', views.cart_list_view, name = 'shopping-cart-list'),
    path('product/<int:id>/add-comment', views.add_comment, name = 'add-comment'),
    path('shop-list/', views.shop_list_view, name = 'shop-list'),
    path('blog/',views.bloggs, name = 'blog'),
    path('about-us/',views.about_us_view,name = 'about-us'),
    path('privacy/',views.privacy, name = 'privacy'),
    path('contact/', views.contact_view, name = 'contact'),
    path('faq/', views.faq, name = 'faq'),
    path('checkout/',views.checkout_view, name = 'checkout'),
    path('complete-order/', views.ordercomplete_view, name = 'order-complete'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('wishlist/delete/<int:id>/', views.wishlist_delete, name='wishlist-delete'),
    path('wishlist/clean/', views.wishlist_clean, name='wishlist-clean'),
    path('cart/clean/', views.cart_list_clean, name = 'cart-list-clean'),
    path('apply-coupon/', views.apply_coupon, name = 'apply-coupon'),
    path('contact/', views.contact_view, name = 'contact'),
    

]