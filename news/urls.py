
from django.urls import path

# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostUpdate, PostDelete, PostSearch, ArticleCreate, ArticleUpdate, ArticleDelete, create_post #PostCreate

urlpatterns = [
   path('', PostList.as_view(), name='posts_list'),
   # pk — это первичный ключ, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:id>', PostDetail.as_view(), name='post_detail'),
   path('create/', create_post, name='create_post'),
   # path('create/', PostCreate.as_view(), name='create_post'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),

]
