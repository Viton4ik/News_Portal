
from django.views.generic.edit import ModelFormMixin, SingleObjectMixin

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404
from pprint import pprint
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, Comment, Author
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm #AuthortForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.models import Group


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

        # get a user id
        context['user_id'] = self.request.user.id
        # get an author id
        context['author_id'] = self.get_object().author.authorUser.id
        # checking - is the user an author
        context['is_author'] = context['user_id'] == context['author_id']
        # checking for the admin rights
        context['admin'] = self.request.user.is_superuser
        # get an author's name
        context['author'] = self.get_object().author.authorUser.username
        # # get a user's name
        context['user_name'] = self.request.user.username

        # to get info in console
        pprint(context)
        print(f"self.object:{self.object}")
        print(f"**kwargs:{kwargs}")
        return context

    # def post(self):
    #     send_mail(
    #         subject=f'Hello there',
    #         message='Hello, my friend!!!',
    #         from_email='NewsPortalSite@yandex.ru',
    #         recipient_list=['mr@victor-vetoshkin.ru']
    #     )
    #
    #     return redirect('appointments:make_appointment')

# add 403.html for def create_post
def html_403(request):
    form = PostForm()
    return render(request, '403.html', {'form' : form})

# page - /news/create/
@permission_required(perm='news.add_post', login_url=html_403) # @login_required(login_url=html_403)
def create_post(request):
    # form = PostForm()
    # if request.method == 'POST':
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #
    #         # # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
    #         # contentType = form.save(commit=False)
    #         # contentType.contentType = 'news'
    #
    #         form.save()
    #         return HttpResponseRedirect('/news') # the page will be after post save
    #
    # return render(request, 'news/post_edit.html', {'form' : form})

    form = PostForm()
    # get user with his id
    user_ = request.user.username
    user_id_ = request.user.id
    # check if admin
    if_admin_ = request.user.is_superuser
    e_mail = request.user.email
    print(f'e_mail: {e_mail}')
    subscribed_categories = Category.objects.filter(subscribers=request.user.id)
    print(f'subscribed_categories: {subscribed_categories}')
    # category = Post._meta.get_field('postCategory').value_from_object(Post.objects.all().values('postCategory'))
    # # post_categories = request.category.name
    # print(f'category: {category}')

    author_group = Group.objects.get(name="authors")
    user_group = request.user.groups.filter()
    print(f'user_group: {user_group}')
    if_author_group = author_group in user_group
    print(f'if_author_group: {if_author_group}')

    # get an author with his id
    # author_field = Post._meta.get_field('author')
    # author_id_ = author_field.value_from_object(Post.objects.first())
    # author_ = Author.objects.filter(id=author_id_)[0]

    author_name = str(*Author.objects.filter(authorUser_id=request.user.id))
    user_is_author = author_name == str(user_)

    author_ = Author.objects.filter(authorUser_id=request.user.id)
    if not author_:
        print(f"'{user_}' is not an author!")
    else:
        print(f"'{user_}' is an author!")
    #     author_name = Author.objects.filter(authorUser_id=request.user.id)[0] #Author.objects.get(author=request.get_object())
    #     print(f"author_name: {author_name} ")
    #     user_is_author = (str(author_name) == str(user_))
    #     print(f'user_is_author: {user_is_author}')

    # create_author = Author.objects.create(authorUser=User.objects.get(username=request.user.username))

    # print(f'author_: {author_}')
    print(f'author_name: {author_name}')
    print(f'user_: {user_}')
    # print(f'user_id_: {user_id_}')
    # print(f'if_admin_: {if_admin_}')
    print(f'user_is_author: {user_is_author}')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # send_mail(
            #     subject=f"{request.POST['topic']}",
            #     message=f"{request.POST['content']}",
            #     from_email='NewsPortalSite@yandex.ru',
            #     recipient_list=[f'{e_mail}'],
            #     # fail_silent=False # - doesn't work with this feature
            # )
            form.save()

            return HttpResponseRedirect('/news') # the page will be after post save

    return render(request, 'news/post_edit.html', {'form': form, 'user_is_author': user_is_author, 'if_author_group': if_author_group})
        # return HttpResponseRedirect('../403/')

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



# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'news/post_edit.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#         )
#         appointment.save()
#         send_mail(
#             subject=f'Hello there',
#             message='Hello, my friend!!!',
#             from_email='NewsPortalSite@yandex.ru',
#             recipient_list=['mr@victor-vetoshkin.ru']
#         )
#         send_mail.send()
#         return redirect('appointments:post_edit')




# class AuthorCreate(CreateView):
#     form_class = AuthortForm
#     model = Post
#     template_name = 'news/author.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['create_user_id'] = self.request.user.id
#         # context['create_author_id'] = self.get_object().author.authorUser.id
#         # context['create_is_author'] = context['create_user_id'] == context['create_author_id']
#         # context['create_author_'] = Author.objects.filter(authorUser_id=self.request.user.id)
#         # if not context['create_author_']:
#         #     Author.objects.create(authorUser=User.objects.get(username=self.request.user.username))
#         # else:
#         #     HttpResponseRedirect('../403/')
#
#         pprint(context)
#         return context





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
        editTime.editTime = datetime.now()
        return super().form_valid(form)

    # in a process!!!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upd_userName'] = self.request.user.username
        context['upd_user_id'] = self.request.user.id
        context['upd_author'] = self.get_object().author.authorUser.username
        context['upd_author_id'] = self.get_object().author.authorUser.id
        context['upd_is_author'] = context['upd_user_id'] == context['upd_author_id']
        context['upd_admin'] = self.request.user.is_superuser

        # if context['upd_is_author']:
        #     Post._meta.get_field('author').widgets{'author': forms.HiddenInput(),}

        #     save_form_data(instance=Post._meta.get_field('author'), data=context['upd_author'])



        # Author1 = User.objects.get(username=self.request.user.username)
        # if context['user_id'] != context['author_id']:
        #     Author.objects.create(authorUser=Author1)

        # get an author's name
        # context['author'] = self.get_object().author.authorUser.username


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

# @login_required
# def update_me(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.group.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#     return redirect('/news')

class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-createTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        context['news_number'] = len(Post.objects.filter(postCategory=self.category))
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = f"You have subscribed to the news in category:"
    return render(request, 'news/subscribe.html', {'category' : category, 'message': message})