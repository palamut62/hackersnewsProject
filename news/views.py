from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Avg
from .models import News, Comment, Rating, Like
from .forms import NewsForm, CommentForm, RatingForm
from functions import time_ago
from django.db.models import Count



def index(request):
    news = News.objects.all().annotate(average_rating=Avg('ratings__rating')).order_by('-date')
    categories = News.objects.values('category').annotate(count=Count('category')).order_by('-count')

    for new in news:
        new.time_ago = time_ago(new.date)
        new.user_liked = new.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'home.html', {'news': news, 'categories': categories})


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
            return redirect('index')  # yorum eklendikten sonra anasayfaya yönlendirme yapılıyor
    comments = Comment.objects.filter(news=news).order_by('-created_at')
    context = {'comments': comments, 'news': news}
    return render(request, 'comments.html', context)



def rating_view(request, rating_id):
    news = get_object_or_404(News, id=rating_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # Kullanıcının daha önce oylama yapmış olup olmadığını kontrol etmek yerine,
            # mevcut oylamayı güncelliyoruz veya yeni bir oylama oluşturuyoruz
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                news=news,
                defaults={'rating': form.cleaned_data['rating']}
            )
            average_rating = news.ratings.aggregate(Avg('rating'))['rating__avg']
            return redirect('index')  # puanlama işlemi tamamlandıktan sonra anasayfaya yönlendirme yapılıyor
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'points.html')

def like_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    like, created = Like.objects.get_or_create(user=request.user, news=news)
    if not created:
        like.delete()
    return redirect('index')

def faq(request):
    return render(request, 'faq.html')

def search_news(request):
    query = request.GET.get('query')
    news = News.objects.filter(title__icontains=query)
    return render(request, 'home.html', {'news': news})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('comment_view', comment.news.id)