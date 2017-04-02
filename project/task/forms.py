# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from task.models import Task


class LoginForm(forms.Form):
    username = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Имя пользователя'}
                    ))
    password = forms.CharField(widget=forms.PasswordInput(
                        attrs={'placeholder': 'Пароль'}
                    ))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня')

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty!', code='login_username')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty!', code='login_password')
        return password

    def clean_remember_me(self):
        remember_me = self.cleaned_data.get('remember_me')
        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = not remember_me
        return remember_me

    def save(self):
        auth = authenticate(**self.cleaned_data)
        return auth


class SignupForm(forms.Form):
    username = forms.CharField(
                max_length=100,
                widget=forms.TextInput(
                    attrs={'placeholder': 'Имя пользователя'}
                ))
    email = forms.EmailField(
                widget=forms.TextInput(
                    attrs={'placeholder': 'Email'}
                ))
    password = forms.CharField(widget=forms.PasswordInput(
                    attrs={'placeholder': 'Пароль'}
                ))

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='signup_username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Email is empty', code='signup_email')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='signup_password')
        return password

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class TaskForm(forms.Form):
    title = forms.CharField(
                max_length=100,
                widget=forms.TextInput(
                    attrs={'placeholder': 'Задача'}
                ))
    estimate = forms.DateField(
                input_formats=['%d.%m.%Y'],
                widget=forms.DateTimeInput(
                    format='%d.%m.%Y',
                    attrs={
                        'class': 'datepicker',
                        'placeholder': 'Дата'
                    }
                ))

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError('Title is empty', code='task_title')
        return title

    """
    def clean_estimate(self):
        estimate = self.cleaned_data['estimate']
        if estimate == '':
            raise forms.ValidationError('Estimate is empty', code='task_estimate')
        return text
    """

    def save(self):
        self.cleaned_data['user'] = self._user
        task = Task(**self.cleaned_data)
        task.save()
        return task