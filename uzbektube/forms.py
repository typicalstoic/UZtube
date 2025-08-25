from django import forms
from .models import VideoContent, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User



class VideoForm(forms.ModelForm):
    class Meta:

        model = VideoContent
        fields = ('title', 'content', 'image', 'video', 'category')
        widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название'
        }),

        'content': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Описание'
        }),
        'image': forms.FileInput(attrs={
            'class': 'form-control',

        }),

        'video': forms.FileInput(attrs={
            'class': 'form-control',

        }),

        'category': forms.Select(attrs={
            'class': 'form-select',
        })
    }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Почтовый адрес', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')



class CommentForm(forms.ModelForm):
    text = forms. CharField(label=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Оставить комменарий'
    }))

    class Meta:
        model = Comment
        fields = ('text',)




class EditAccountForm(UserChangeForm):
    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    old_password = forms.CharField(required=False, label= 'Old password', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password = forms.CharField(required=False, label='New password', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(required=False, label='Confirm new password ', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'old_password', 'new_password', 'confirm_password')

class EditProfileForm(forms.ModelForm):
    name = forms.CharField(label='Profile Name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    nick_name = forms.CharField(label='Profile nickname', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    photo = forms.ImageField(label='Profile picture', widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Profile
        fields = ('name', 'nick_name', 'photo')
