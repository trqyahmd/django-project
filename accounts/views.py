from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm, CustomPasswordChangeForm, ResetPasswordForm, ResetPasswordSuccessForm,AddressForm
from django.contrib.auth import authenticate, login, logout
from .models import Profile, User
from services.generator import CodeGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# def login_view(request):

#     form = LoginForm()

#     if request.method == "POST":
#         form = LoginForm(request.POST or None)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
            

#             user = authenticate(username=username, password=password)

#             login(request, user)

#             return redirect('/')
        
    
#     context = {
#         'form' : form
#     }

#     return render(request,'accounts/login.html',context)

# def login_view(request):
#     form = LoginForm()

#     if request.method == "POST":
#         form = LoginForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = authenticate(request, username=username, password=password)

#             if user is not None and user.is_active:
#                 login(request, user)
#                 return redirect('/')
#             else:
#                 form.add_error(None, 'Invalid username or password')

#     context = {
#         'form': form
#     }

#     return render(request, 'accounts/login.html', context)

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("/products/home/")
            # if user is not None and user.is_active:
            #     login(request, user)
            #     return redirect('/')
            # else:
            #     form.add_error(None, 'Invalid username or password')

    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    redirect ('/')
    
    return HttpResponseRedirect('/products/home/')



# def register_view(request):
#     form = RegisterForm()

#     if request.method == "POST":
#         form = RegisterForm(request.POST or None)
        

#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.is_active = False
#             password = form.cleaned_data.get('password')
#             new_user.set_password(password)
#             new_user.save()
#             profile = Profile.objects.create(
#                 user = new_user,
#                 activation_link = CodeGenerator.create_activation_link_code(
#                 size=30, model_=Profile
#                 )
#             )

#             link = request.build_absolute_uri(f'/accounts/activate/account/{profile.activation_link}/')

#             message = f'Zəhmət olmasa hesabınızı aktivləştirmək üçün aşağıdakı linkdən istifadə edin: {link}'

#             # sending authentication mail (confirmation)

#             send_mail(
#                 'E-mail identifikasiyası ilə hesabınızı aktivləşdirin',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [new_user.email],
#                 fail_silently=False
#             )

#             return redirect('/products/home/')
        
#     context = {

#         'form' : form
#     }

#     return render(request, 'accounts/register.html', context)

from django.shortcuts import render, redirect
from django.http import HttpResponse
import time

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            password = form.cleaned_data.get('password')
            new_user.set_password(password)
            new_user.save()
            profile = Profile.objects.create(
                user=new_user,
                activation_link=CodeGenerator.create_activation_link_code(size=30, model_=Profile)
            )

            link = request.build_absolute_uri(f'/accounts/activate/account/{profile.activation_link}/')
            message = f'Zəhmət olmasa hesabınızı aktivləştirmək üçün aşağıdakı linkdən istifadə edin: {link}'

            send_mail(
                'E-mail identifikasiyası ilə hesabınızı aktivləşdirin',
                message,
                settings.EMAIL_HOST_USER,
                [new_user.email],
                fail_silently=False
            )

            return redirect('/accounts/email_sent/') 

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


def activate_account(request, activation_link):
    profile = get_object_or_404(Profile, activation_link = activation_link)
    profile.user.is_active = True
    profile.user.save()
    return redirect('/accounts/login/')


@login_required(login_url='/accounts/login/')
def password_change_view(request):
    form = CustomPasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user = request.user, data = request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:login')
        
    context = {
        'form' : form
    }

    return render(request, 'accounts/password_change.html', context)



def reset_password_view(request):

    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email = email)
            

            link = request.build_absolute_uri(reverse_lazy("accounts:reset-password-success", kwargs = {"slug" : user.slug}))
            message = f'Şifrəni sıfırlamaq üçün aşağıdakı linkdən istifadə edin \n{link}'

            

            send_mail(
                'Şifrə sıfırlama', 
                message,
                settings.EMAIL_HOST_USER, 
                [email], 
                fail_silently=False 

            )

            return redirect('/accounts/login/')
    
    context = {
        'form' : form
    }

    return render(request, 'accounts/password_reset.html', context)

# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes

# def reset_password_view(request):
#     form = ResetPasswordForm()

#     if request.method == "POST":
#         form = ResetPasswordForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             user = User.objects.get(email=email)

#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             print("Generated Token:", token)  # Print the token to verify

            
#             # link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': uid, 'token': token}))
#             link = request.build_absolute_uri(reverse('accounts:reset-password', kwargs={'uidb64': uid, 'token': token}))


#             message = f'Şifrəni sıfırlamaq üçün aşağıdakı linkdən istifadə edin:\n{link}'

#             send_mail(
#                 'Şifrə sıfırlama',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False
#             )

#             return redirect('/accounts/login/')

#     context = {
#         'form': form,
#         'user_id': user.id,
#         'reset_token': token,

#     }

#     return render(request, 'accounts/password_reset.html', context)


def reset_password_success(request, slug):

    user = get_object_or_404(User, slug = slug)
    form = ResetPasswordSuccessForm(instance = user)
    
    if request.method == "POST":

        form = ResetPasswordSuccessForm(instance = user, data = request.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")

    context = {
        "form" : form
    }

    return render(request, 'accounts/reset_succes.html', context)

@login_required
def profileinfo_view(request):

    context = {

    }

    return render(request, 'accounts/profile-info.html', context)


def email_sent_view(request):

    return render(request, 'accounts/email_sent.html')


def create_address(request):
    form = AddressForm()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.address = request.user
            address.save()
            return redirect('accounts:address-list')
    else:
        form = AddressForm()

    context = {
        'form': form,

    }

    return render(request, 'accounts/address-add.html')


def addresses_list(request):

    context = {

    }

    return render(request, 'accounts/addresses.html', context)
