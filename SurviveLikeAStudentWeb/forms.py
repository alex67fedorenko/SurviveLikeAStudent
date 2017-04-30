# -*- coding: utf-8 -*-
__author__ = 'afedorenko'
from django import forms
from .models import Post, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    passw = forms.CharField(widget=forms.PasswordInput, label='Password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'full_name', 'about')
