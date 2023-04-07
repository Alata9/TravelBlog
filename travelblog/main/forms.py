from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import *


# личные данные пользователя
class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


# регистрация пользователя
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')


#  форма надрубрики
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SubRubric.object.all(), empty_label=None, label='Super_rubric', required=False)

    class Meta:
        model = SubRubric
        fields = '__all__'


# форма поиска по контексту
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=50, label='')


# форма добавления записи и набор форм
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = ['rubric', 'title', 'content', 'is_active', 'image']
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}

AIFormSet = inlineformset_factory(Article, AdditionalImage, fields='__all__')

