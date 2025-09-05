
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post
from .models import UserProfile
from .models import Comment
from .models import Requote

class PostForm (forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control my-2',
                'placeholder':'Enter Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control my-2',
                'placeholder': 'Write your content',
                'rows': 5
            }),
        }



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control border-0 bg-bluelight', 'placeholder': 'Username'}), help_text=""
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control border-0 bg-bluelight', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control border-0 bg-bluelight', 'placeholder': 'Confirm Password'})
    )



    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-0 bg-bluelight', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-0 bg-bluelight', 'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'email': 'Email',
        }
        widgets = {
            'username': forms.HiddenInput(attrs={'class': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0 bg-bluelight'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image']
        labels = {
            'profile_image': 'Profile',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control border-0 bg-bluelight', 'rows': 3}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control form-control-sm border-0 bg-white '}),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'})
        }




class RequoteForm(forms.ModelForm):
    class Meta:
        model = Requote
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a caption...'}),
        }