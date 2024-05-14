from django import forms
from .models import News, Comment, Rating

class NewsForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={
            'required': 'Please enter a title.',
            'invalid': 'This is not a valid title.',
        }
    )

    class Meta:
        model = News
        fields = ['title', 'short_description', 'link', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
