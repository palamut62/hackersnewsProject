from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import News, Comment, Rating, Like


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'date','category')
    list_filter = ['date']
    search_fields = ['title']

admin.site.register(News)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'comment')
    list_filter = ['news']
    search_fields = ['comment']

admin.site.register(Comment)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'rating')
    list_filter = ['news']
    search_fields = ['rating']

admin.site.register(Rating)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('news', 'user')
    list_filter = ['news']
    search_fields = ['user']

admin.site.register(Like)