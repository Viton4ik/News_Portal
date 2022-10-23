
from datetime import datetime
from django.shortcuts import render
from pprint import pprint

'''дженерик ListView, который реализует вывод списка объектов модели, используя указанный шаблон. 
А вот какую модель, как и в какой шаблон выводить, мы должны указать сами'''

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post
from .models import Category
from .models import PostCategory

class PostList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-createTime'

    # or we can sort fields
    # queryset = Post.objects.filter(rating__gt=2)
    # queryset = Product.objects.order_by('name')

    template_name = 'news/news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        # context['next_sale'] = "Распродажа в среду!"
        pprint(context) # to get info in console
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news/content.html'
    context_object_name = 'content'
    pk_url_kwarg = 'id'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['category'] = Post.objects.get(id='postThrough').postCategory.add(Category.objects.get(id='postCategory'))
    #     # # context['category'] = PostCategory.objects.filter(postThrough=Post.objects.get('id')).values('name')
    #     # context['category'] = Category.objects.filter(post__topic='topic')
    #     # context['post'] = Post.objects.exclude(self.topic)
    #     # context['postThrough'] = PostCategory.objects.values('postThrough')
    #     # context['categoryThrough'] = PostCategory.objects.values('categoryThrough')
    #     pprint(context) # to get info in console
    #     return context

