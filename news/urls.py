
from django.urls import path

# Импортируем созданное нами представление
from .views import PostList, PostDetail

urlpatterns = [
   path('', PostList.as_view()),
   # pk — это первичный ключ, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # path('<int:pk>', ProductDetail.as_view()), #default
   path('<int:id>', PostDetail.as_view()),

]
