from django.urls import path
from .views import index, add_news, edit_news, comment_view, rating_view, like_view, faq, search_news, delete_comment

urlpatterns = [
    path('', index, name='index'),
    path('add_news/', add_news, name='add_news'),
    path('edit_news/<int:news_id>/', edit_news, name='edit_news'),
    path('comment/<int:comment_id>/', comment_view, name='comment_view'),
    path('rating/<int:rating_id>/', rating_view, name='rating_view'),
    path('like/<int:news_id>/', like_view, name='like_view'),
    path('faq/', faq, name='faq'),
    path('search-news/', search_news, name='search_news'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment')

]
