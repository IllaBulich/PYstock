from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation  
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


class UserPasswordForm(PasswordChangeForm):  
    old_password = forms.CharField(  
        max_length=128,  
        label='Старый пароль',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите старый пароль'  
        })  
    )  
    new_password1 = forms.CharField(  
        max_length=128,  
        label='Новый пароль',  
        help_text=password_validation.password_validators_help_text_html(),  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите новый пароль'  
        })  
    )  
    new_password2 = forms.CharField(  
        max_length=128,  
        label='Подтверждение нового пароля',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Повторите новый пароль'  
        })  
    )


class UserInfoForm(forms.ModelForm):  
    username = forms.CharField(  
        max_length=150,  
        label='Имя пользователя (username)',  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите имя пользователя'  
        })  
    )  
    email = forms.EmailField(  
        widget=forms.EmailInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите email'  
        })  
    )  
    first_name = forms.CharField(  
        max_length=150,  
        label='Имя',  
        required=False,  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите ваше имя'  
        })  
    )  
    last_name = forms.CharField(  
        max_length=150,  
        label='Фамилия',  
        required=False,  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите вашу фамилию'  
        })  
    )  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'first_name', 'last_name']


class CustomPasswordResetForm(PasswordResetForm):  
    email = forms.EmailField(  
        label="Email",  
        max_length=254,  
        widget=forms.EmailInput(  
            attrs={'class': 'form-control',  
                   'placeholder': 'Введите Email',  
                   "autocomplete": "email"}  
        )  
    )  


class CustomSetPasswordForm(SetPasswordForm):  
    error_messages = {  
        "password_mismatch": "Пароли не совпадают"  
    }  
    new_password1 = forms.CharField(  
        label='Новый пароль',  
        widget=forms.PasswordInput(  
            attrs={'class': 'form-control',  
                   'placeholder': 'Введите новый пароль',  
                   "autocomplete": "new-password"}  
        ),  
        strip=False,  
        help_text=password_validation.password_validators_help_text_html(),  
    )  
    new_password2 = forms.CharField(  
        label='Подтверждение нового пароля',  
        strip=False,  
        widget=forms.PasswordInput(  
            attrs={'class': 'form-control',  
                   'placeholder': 'Подтвердите новый пароль',  
                   "autocomplete": "new-password"}  
        ),  
    )


class RegistrationForm(UserCreationForm):  
    username = forms.CharField(  
        max_length=150,  
        label='Имя пользователя',  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите имя пользователя'  
        })  
    )  
    email = forms.EmailField(  
        widget=forms.EmailInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите email'  
        })  
    )  
    password1 = forms.CharField(  
        max_length=128,  
        label='Пароль',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите пароль'  
        })  
    )  
    password2 = forms.CharField(  
        max_length=128,  
        label='Подтверждение пароля',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Повторите пароль'  
        })  
    )  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'password1', 'password2', ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']