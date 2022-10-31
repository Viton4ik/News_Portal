
from datetime import datetime
from django.shortcuts import render
from pprint import pprint
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, Comment, Author
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

class PostList(ListView):
    model = Post
    ordering = '-createTime'

    # or we can sort fields
    # queryset = Post.objects.filter(rating__gt=2)
    # queryset = Product.objects.order_by('name')

    template_name = 'news/news.html'
    context_object_name = 'news'
    # количество записей на странице
    paginate_by = 8

    # Переопределяем функцию получения списка
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        pprint(self.filterset)  # to get info in console
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # all amount of news
        context['news_number'] = len(Post.objects.all())
        # get filterset
        context['filterset'] = self.filterset
        # to get info in console
        pprint(context)
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news/content.html'
    context_object_name = 'content'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get comments
        context['comments'] = Comment.objects.filter(commentPost=self.object)
        # to get comment_user - doesn't work properly!
        context['commentUser'] = User.objects.filter(username=self.object)
        # to get category
        context['categories'] = Category.objects.filter(post=self.object)
        # to get info in console
        pprint(context)
        return context

        # user = User.objects.get(id=request.user.id)
        # author = Author.objects.get(user=user)

# page - /news/create/
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
            contentType = form.save(commit=False)
            contentType.contentType = 'news'

            form.save()
            return HttpResponseRedirect('/news') # the page will be after post save
    return render(request, 'news/post_edit.html', {'form' : form})

# # page - /news/create/
# class PostCreate(CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'news/post_edit.html'
#
#     # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
#     # Далее super().form_valid(form) запустит стандартный механизм сохранения, который вызовет form.save(commit=True)
#     def form_valid(self, form):
#         contentType = form.save(commit=False)
#         contentType.contentType = 'news'
#         return super().form_valid(form)


# или через generic
# page - /articles/create/
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
    # Далее super().form_valid(form) запустит стандартный механизм сохранения, который вызовет form.save(commit=True)
    def form_valid(self, form):
        contentType = form.save(commit=False)
        contentType.contentType = 'post'
        return super().form_valid(form)

# page - /news/edit/
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


# page - /articles/edit/
class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


# page - /news/delete/
class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts_list')


# page - /articles/delete/
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts_list')


# page - /news/search
class PostSearch(ListView):
    model = Post
    ordering = '-createTime'
    template_name = 'news/post_search.html'
    context_object_name = 'news'
    paginate_by = 10

    # Переопределяем функцию получения списка
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()

        # total amount of news that have been found
        context['news_number'] = len(self.filterset.qs)

        context['filterset'] = self.filterset
        pprint(context)
        return context

    # def clean_filters(request):
    #    number = request.GET.get('number')
    #    multiplier = request.GET.get('multiplier')
    #
    #    try:
    #        result = int(number) * int(multiplier)
    #        html = f"<html><body>{number}*{multiplier}={result}</body></html>" #?number=3&multiplier=2
    #    except (ValueError, TypeError):
    #        html = f"<html><body>Invalid input.</body></html>"
    #
    #    return HttpResponse(html) #?topic__contains=&author=&createTime_filer=

    # def clean_filters(request):
    #    html = f"<html><body>topic__contains=&author=&createTime_filer=</body></html>"
    #    return HttpResponse(html) #?topic__contains=&author=&createTime_filer=