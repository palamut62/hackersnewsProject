from django import forms
from .models import News

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


