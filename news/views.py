from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Avg
from .models import News, Comment, Rating, Like
from .forms import NewsForm, CommentForm, RatingForm
from functions import time_ago



def index(request):
    news = News.objects.all().annotate(average_rating=Avg('ratings__rating'))
    for new in news:
        new.time_ago = time_ago(new.date)
        new.user_liked = new.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'home.html', {'news': news})


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
        return JsonResponse({'status': 'success', 'comments': comments_data})


def rating_view(request, rating_id):
    news = get_object_or_404(News, id=rating_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                news=news,
                defaults={'rating': form.cleaned_data['rating']}
            )
            average_rating = news.ratings.aggregate(Avg('rating'))['rating__avg']
            return JsonResponse({'status': 'success', 'rating': average_rating})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def search_news(request):
    query = request.GET.get('q', '')
    if query:
        results = News.objects.filter(title__icontains=query)
    else:
        results = News.objects.all()

    results_data = []
    for news in results:
        results_data.append({
            'id': news.id,
            'title': news.title,
            'short_description': news.short_description,
            'link': news.link,
            'category': news.category,
            'average_rating': news.ratings.aggregate(Avg('rating'))['rating__avg'] or 0,
            'comments_count': news.comments.count(),
            'likes_count': news.likes.count(),
            'user_liked': news.likes.filter(user=request.user).exists() if request.user.is_authenticated else False,
            'time_ago': time_ago(news.date)
        })

    return JsonResponse({'results': results_data})



def like_view(request, news_id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=news_id)
        like, created = Like.objects.get_or_create(news=news, user=request.user)
        if not created:
            like.delete()
            user_liked = False
        else:
            user_liked = True
        return JsonResponse({'status': 'success', 'likes_count': news.likes.count(), 'user_liked': user_liked})
    else:
        return JsonResponse({'status': 'error', 'message': 'User is not authenticated'})


def faq(request):
    return render(request, 'faq.html')