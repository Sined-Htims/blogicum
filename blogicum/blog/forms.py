from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comments

User = get_user_model()


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'is_superuser',
            'is_staff', 'is_active', 'date_joined',
            'groups', 'user_permissions',
        )
    # Стандартная форма для редактирования данных пользователя:
    # UserChangeForm из from django.contrib.auth.forms import UserChangeForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': '22', 'rows': '5'})
        }
