from django import forms
from .models import News, Comment

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


from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

