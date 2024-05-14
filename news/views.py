from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Avg
from .models import News, Comment, Rating
from .forms import NewsForm, CommentForm, RatingForm
from functions import time_ago

def index(request):
    news_list = News.objects.all()
    for news in news_list:
        news.time_ago = time_ago(news.date)
        news.average_rating = news.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'home.html', {'news': news_list})

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

def comment_view(request, comment_id):
    news = get_object_or_404(News, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()
            comments = Comment.objects.filter(news=news).order_by('-created_at')
            comments_data = serializers.serialize('json', comments)
            return JsonResponse({'status': 'success', 'comments': comments_data, 'comments_count': comments.count()})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    elif request.method == 'GET':
        comments = Comment.objects.filter(news=news).order_by('-created_at')
        comments_data = serializers.serialize('json', comments)
        return JsonResponse({'status': 'success', 'comments': comments_data, 'comments_count': comments.count()})

def rating_view(request, rating_id):
    news = get_object_or_404(News, id=rating_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.news = news
            rating.save()
            average_rating = Rating.objects.filter(news=news).aggregate(Avg('rating'))['rating__avg'] or 0
            return JsonResponse({'status': 'success', 'rating': average_rating})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
