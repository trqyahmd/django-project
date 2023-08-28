from django import forms
from .models import Profile, User, Addresses
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput, label = "Şifrə")

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control',
                'placeholder' : f'{self.fields[field].label}',
            })

    def clean(self):
        attrs = self.cleaned_data

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username = username, password = password)
        
        if not user:
            raise forms.ValidationError('Bu istifadəçi mövcud deyil!')
        
        if not user.is_active:
            raise forms.ValidationError('Bu istifadəçi aktiv deyil!')
        
        if not user.check_password(password):
            raise forms.ValidationError('İstifadəçi şifrəsi yanlışdır')
        
        if not username:
            raise forms.ValidationError('Zəhmət olmasa istifadəçi adını daxil edin!')
        
        if not password:
            raise forms.ValidationError('Zəhmət olmasa şifrəni daxil edin!')
        
        if username and username.upper() == username and not any(c.islower() for c in username):
            raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur istifadəçi adını daxil etməmişdən öncə söndürəsiniz!.'))
        
        if password and password.upper() == password and not any(c.islower() for c in password):
            raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur şifrə daxil etməmişdən öncə söndürəsiniz!.'))
        
        return attrs
    

# class RegisterForm(forms.ModelForm):

#     password = forms.CharField(widget = forms.PasswordInput, label = "Şifrə")
#     password_confirm = forms.CharField(widget = forms.PasswordInput, label = "Şifrə Təsdiqi")

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({
#                 'class' : 'form-control',
#                 'placeholder' : f'{self.fields[field].label}'
#             })


#     def clean(self):
#         attrs = self.cleaned_data

#         username = attrs.get('username')
#         password = attrs.get('password')
#         password_confirm = attrs.get('password_confirm')

#         user = authenticate(username=username, password = password)

#         if user:
#             raise forms.ValidationError('Bu istifadəçi adı artıq mövcuddur!')
        
#         if len(password) < 10:
#             raise forms.ValidationError('Şifrə ən az 10 simvoldan ibarət olmalıdır')
        
#         if password != password_confirm:
#             raise forms.ValidationError('Şifrələr uyğun deyil!')
        
#         if not password.strip()[0].isalpha():
#             raise forms.ValidationError('Şifrə hərflə başlamalıdır!')
        
#         if not password.isalnum():
#             raise forms.ValidationError('Şifrə hərflərdən və rəqəmlərdən ibarət olmalıdır!')
        
#         if username and username.upper() == username and not any(c.islower() for c in username):
#             raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur istifadəçi adını daxil etməmişdən öncə söndürəsiniz!.'))
        
#         if password and password.upper() == password and not any(c.islower() for c in password):
#             raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur şifrə daxil etməmişdən öncə söndürəsiniz!.'))
        
#         if password_confirm and password_confirm.upper() == password_confirm and not any(c.islower() for c in password_confirm):
#             raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur şifrə daxil etməmişdən öncə söndürəsiniz!.'))
        
#         if not username:
#             raise forms.ValidationError('İstifadəçi adı boş saxlanıla bilməz!')
        
#         if not password:
#             raise forms.ValidationError('Şifrə boş saxlanıla bilməz!')
        
#         return attrs

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput, label = "Şifrə")
    password_confirm = forms.CharField(widget = forms.PasswordInput, label = "Şifrə Təsdiqi")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control',
                'placeholder' : f'{self.fields[field].label}'
            })

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     error_class = 'has-error' if self.errors else ''

    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class': f'form-control {error_class}',
    #             'placeholder' : f'{self.fields[field].label}'
    #         })

    def clean(self):
        attrs = self.cleaned_data

        username = attrs.get('username')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        # user = authenticate(username=username, password = password)
        user_qs = User.objects.filter(username=username)

        if user_qs.exists():
            raise forms.ValidationError('Bu istifadəçi adı artıq mövcuddur!')
        
        if len(password) < 10:
            raise forms.ValidationError('Şifrə ən az 10 simvoldan ibarət olmalıdır!')
        
        if password != password_confirm:
            raise forms.ValidationError('Şifrələr uyğun deyil!')
        
        if not password.strip()[0].isalpha():
            raise forms.ValidationError('Şifrə hərflə başlamalıdır!')
        
        if not password.isalnum():
            raise forms.ValidationError('Şifrə hərflərdən və rəqəmlərdən ibarət olmalıdır!')
        
        if username and username.upper() == username and not any(c.islower() for c in username):
            raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur istifadəçi adını daxil etməmişdən öncə söndürəsiniz!.'))
        
        if password and password.upper() == password and not any(c.islower() for c in password):
            raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur şifrə daxil etməmişdən öncə söndürəsiniz!.'))
        
        if password_confirm and password_confirm.upper() == password_confirm and not any(c.islower() for c in password_confirm):
            raise forms.ValidationError(_('Caps Lock yanılıdır. Xahiş olunur şifrə daxil etməmişdən öncə söndürəsiniz!.'))
        
        if not username:
            raise forms.ValidationError('İstifadəçi adı boş saxlanıla bilməz!')
        
        if not password:
            raise forms.ValidationError('Şifrə boş saxlanıla bilməz!')
        
        return attrs
    

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })


class ResetPasswordForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ('email', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

    def clean(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError('Bu E-poçt ünvanı möcud deyil!')
        return self.cleaned_data

class ResetPasswordSuccessForm(forms.Form):
    password1 = forms.CharField(widget = forms.PasswordInput, label = 'Şifrə')
    password2 = forms.CharField(widget = forms.PasswordInput, label = 'Şifrə Təsdiqi')

    class Meta:
        model = User
        fields = ("password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(password1.strip()) < 6:
            raise forms.ValidationError('Düzgün şifrəni daxil edin!')
        
        if password1 != password2:
            raise forms.ValidationError('Şifrələr uyğun deyil')
        
        return self.cleaned_data
    
    def save(self):
        password1 = self.cleaned_data.get("password1")
        self.instance.set_password(password1)
        self.instance.save()
        return self.instance

class AddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ['telephone', 'country', 'city', 'street', 'zip_code']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control',
                'placeholder' : f'{self.fields[field].label}',
            })
