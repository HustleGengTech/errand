from django import forms
from .models import Profile, Post,Comment,Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'fullname','city','state','country','occupation','socials','bio', ]  # Fields users can edit

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']  # Fields for the post form

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']  # Fields for the post form

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label="New Email", required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email is already in use.")
        return new_email
