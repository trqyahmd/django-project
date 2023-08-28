from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/', views.register_view, name = 'register'),
    path('activate/account/<activation_link>/', views.activate_account, name = 'activate-account'),
    path('change-password/', views.password_change_view, name = 'change-password'),
    # path('reset-password/', views.reset_password_view, name = 'reset-password'),
    # path('reset-password-success/<slug>/', views.reset_password_success, name = 'reset-password-success'),
    path('profile-info/', views.profileinfo_view, name = 'profile-info'),
    path('email_sent/', views.email_sent_view, name = 'email_sent'),
    # path('reset/<str:uidb64>/<str:token>/', views.reset_password_view, name='reset-password'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('address-add/', views.create_address, name = 'address-add'),
    path('addresses/', views.addresses_list, name = 'addresses'),
]