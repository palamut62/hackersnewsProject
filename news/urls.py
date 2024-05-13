from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_news/', views.add_news, name='add_news'),
    path('edit_news/<int:news_id>/', views.edit_news, name='edit_news'),
    path('comment/<int:comment_id>/', views.comment_view, name='comment_view'),

]
