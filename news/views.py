

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
        # get the user
        context['user'] = self.request.user.username
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
        # context['comments'] = Comment.objects.filter(commentPost=self.object)
        # to get comment_user - doesn't work properly!
        # context['commentUser'] = User.objects.filter(comment=context['comments'][0])

        # to get comments + username
        comment_user = []
        comments = Comment.objects.filter(commentPost=self.object)
        for i, comment in enumerate(comments):
            comment_user.append(f"{User.objects.filter(comment=comments[i])[0]}: '{comments[i]}'")
        context['comments'] = comment_user

        # to get category
        context['categories'] = Category.objects.filter(post=self.object)
        # to get info in console
        pprint(context)
        print(f"self.object:{self.object}")
        print(f"**kwargs:{kwargs}")
        return context

# add 403.html for def create_post
def html_403(request):
    form = PostForm()
    return render(request, '403.html', {'form' : form})

# page - /news/create/
@permission_required(perm='news.add_post', login_url=html_403) # @login_required(login_url=html_403)
def create_post(request):
    # raise_exception = True
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            # # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
            # contentType = form.save(commit=False)
            # contentType.contentType = 'news'

            form.save()
            return HttpResponseRedirect('/news') # the page will be after post save
    return render(request, 'news/post_edit.html', {'form' : form})

# или через generic
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


# page - /news/edit/
class PostUpdate(PermissionRequiredMixin, UpdateView): #class PostUpdate(LoginRequiredMixin, UpdateView):
    # rights providing
    permission_required = ('news.change_post',)

    # show 403.html
    raise_exception = True

    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    # save last editing time for the post
    def form_valid(self, form):
        editTime = form.save(commit=False)
        # author_id = form.save(commit=False)
        editTime.editTime = datetime.now()
        # author_id.id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.username
        context['author'] = Author.objects.get(post=self.get_object())#self.get_object()
        context['user_id'] = self.request.user.id
        context['author_id'] = self.get_object().author.authorUser.id
        pprint(context)
        print(f"self.object:{self.object}")
        print(f"**kwargs:{kwargs}")
        return context


# page - /news/delete/
class PostDelete(PermissionRequiredMixin, DeleteView): # class PostDelete(LoginRequiredMixin, DeleteView):
    # rights providing
    permission_required = ('news.delete_post',)

    # show 403.html
    raise_exception = True

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
