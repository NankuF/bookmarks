from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    """Форма авторизации"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Форма позволит пользователям менять имя, фамилию, e-mail"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Форма позволит модифицировать дополнительные сведения,
        которые мы сохраняем в модели Profile"""

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
