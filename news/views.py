# news/views.py

# news/views.py

from django.shortcuts import render, redirect, get_object_or_404
from functions import time_ago
from news.models import News

def index(request):
    news = News.objects.all()
    for new in news:
        new.time_ago = time_ago(new.date)
    return render(request, 'home.html', {'news': news})



from .forms import NewsForm

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})


def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    else:
        form = NewsForm(instance=news)
    return render(request, 'add_news_edit.html', {'form': form})