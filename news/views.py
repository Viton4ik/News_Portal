from django.shortcuts import render

from django.shortcuts import render

'''дженерик ListView, который реализует вывод списка объектов модели, используя указанный шаблон. 
А вот какую модель, как и в какой шаблон выводить, мы должны указать сами'''

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-createTime'

    # or we can sort fields
    # queryset = Post.objects.filter(rating__gt=2)
    # queryset = Product.objects.order_by('name')

    template_name = 'news/news.html'
    context_object_name = 'list'

class PostDetail(DetailView):
    model = Post
    template_name = 'news/content.html'
    context_object_name = 'content'
    pk_url_kwarg = 'id'