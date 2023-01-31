from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'information', 'password1', 'password2', 'email', 'description', 'avatar',]
        widget = {
            'avatar': forms.ImageField,
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'information': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш никнейм"})
        self.fields['information'].widget.attrs.update({'class': 'form-control', 'placeholder': "информация о пользователе"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль ещё раз"})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5, 'placeholder': "введите описание вашего профиля"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш адрес эл. почты"})
        self.fields['avatar'].widget.attrs.update({'null': 'photos/user.png', 'placeholder': "ваш аватар"})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


# class CustomUserChangePasswordForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ['password1', 'password2']
#         widget = {
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(CustomUserChangePasswordForm, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль ещё раз"})
#
#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].help_text = None


# class CustomUserChangePassword(forms.Form):
#     password1 = forms.PasswordInput(attrs={'class': 'form-control'}),
#     password2 = forms.PasswordInput(attrs={'class': 'form-control'}),
#
#     def __init__(self, *args, **kwargs):
#         super(CustomUserChangePassword, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш новый пароль"})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль ещё раз"})


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'information', 'description', 'avatar']
        widget = {
            'avatar': forms.ImageField,
            'information': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш никнейм", 'blank': True})
        self.fields['information'].widget.attrs.update({'class': 'form-control', 'placeholder': "информация о пользователе"})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите статус вашего профиля"})
        self.fields['avatar'].widget.attrs.update({})

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None


class ProfileForm(forms.Form):
    information = forms.TextInput(attrs={'class': 'form-control'})
    description = forms.TextInput(attrs={'class': 'form-control'})
    avatar = forms.ImageField(label='avatar', required=False)


class CustomChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'information', 'description']


class UserLoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})),
    email = forms.EmailField,
    password1 = forms.CharField,
    password2 = forms.CharField,

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'введите ваш никнейм'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text',]
        widget = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            #'answer_by': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': 10, 'placeholder': 'Введите текст комментария'})
        #self.fields['answer_by'].widget.attrs.update({'class': 'form-control'})
