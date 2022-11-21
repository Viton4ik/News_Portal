
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
<<<<<<< HEAD
from datetime import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404
from pprint import pprint
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, Category, Comment, Author
=======
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect, get_object_or_404
from pprint import pprint
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, Comment, Author, PostCategory
>>>>>>> dev
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from datetime import datetime, timedelta



class PostList(ListView):
    model = Post
    ordering = '-createTime'
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
        return context

# add 403.html for def create_post
def html_403(request):
    form = PostForm()
    return render(request, '403.html', {'form' : form})

# page - /news/create/
@permission_required(perm='news.add_post', login_url=html_403)
def create_post(request):
<<<<<<< HEAD
    form = PostForm()

    # get user with his id
    user_ = request.user.username
    user_id_ = request.user.id

    # check if admin
    if_admin_ = request.user.is_superuser
    e_mail = request.user.email

    subscribed_categories = Category.objects.filter(subscribers=request.user.id)
    author_group = Group.objects.get(name="authors")
    user_group = request.user.groups.filter()
    if_author_group = author_group in user_group
    author_name = str(*Author.objects.filter(authorUser_id=request.user.id))
    user_is_author = author_name == str(user_)
    author_ = Author.objects.filter(authorUser_id=request.user.id)
=======
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

    # get the user
    user_ = request.user.username
    author_name_ = Author.objects.filter(authorUser_id=request.user.id)
    author_name = str(*Author.objects.filter(authorUser_id=request.user.id)) if not request.user.is_superuser else f"Admin: <{request.user.username}>"
    # check if the user is an author
    user_is_author = author_name == str(user_)

    # check if admin
    # if_admin_ = request.user.is_superuser

    # print an e-mail to check
    e_mail = request.user.email
    print(f'e_mail: {e_mail}')

    # get user's subscriber categoties
    subscribed_categories = Category.objects.filter(subscribers=request.user.id)
    print(f'subscribed_categories: {subscribed_categories}')

    # get group 'authors'
    author_group = Group.objects.get(name="authors")
    # get all users' groups
    user_group = request.user.groups.filter()
    # check if user is in the 'authors' group
    is_author_group = author_group in user_group

    # get authors list
    author_list = Author.objects.all()

    # print(f"form: {form['author']}")

    # to show my time zone
    from django.utils import timezone
    print(f"timezone: {timezone.now()}")
>>>>>>> dev

    if request.method == 'POST':
        form = PostForm(request.POST)


        if form.is_valid():
<<<<<<< HEAD
=======

            # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
            author = form.save(commit=False)
            # if not an admin
            if not request.user.is_superuser:
                author.author = Author.objects.get(authorUser_id=request.user.id)
            else:
                # if admin - author has to be chosen
                author_user = User.objects.get(username=request.POST['author'])
                author.author = Author.objects.get(authorUser_id=author_user.id)

            # send_mail(
            #     subject=f"{request.POST['topic']}",
            #     message=f"{request.POST['content']}",
            #     from_email='NewsPortalSite@yandex.ru',
            #     recipient_list=[f'{e_mail}'],
            #     # fail_silent=False # - doesn't work with this feature
            # )

>>>>>>> dev
            form.save()
            return HttpResponseRedirect('/news') # the page will be after post save
<<<<<<< HEAD
    return render(request, 'news/post_edit.html', {'form': form})
=======

    return render(request, 'news/post_edit.html', {
        'form': form,
        'user_is_author': user_is_author,
        'is_author_group': is_author_group,
        'author_name': author_name,
        'author_list': list(author_list),
    })

# author_create function
def author_create(request):
    user_id = request.user.id
    authors_list_id = Author.objects.all().values_list('authorUser', flat=True)
    if user_id not in authors_list_id:                        # if user is not an author
        author = Author.objects.create(authorUser_id=user_id) # create a new author
        authors_group = Group.objects.get(name="authors")     # put him in group 'authors'
        request.user.groups.add(authors_group)                # put him in group 'authors'
        message = f"Congratulations! '{request.user}' has become an Author!"
    else:
        author = user_id
        message = f"'{request.user}' is already an Author!"
    return render(request, 'news/author_create.html', {'category': author, 'message': message})


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
>>>>>>> dev


# page - /news/edit/
class PostUpdate(PermissionRequiredMixin, UpdateView):
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
        author = form.save(commit=False)
        # if not an admin
        if not self.request.user.is_superuser:
            author.author = Author.objects.get(authorUser_id=self.request.user.id)
        else:
            # if admin - author has to be chosen
            author_user = User.objects.get(username=self.request.POST['author'])
            author.author = Author.objects.get(authorUser_id=author_user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upd_user_id'] = self.request.user.id
        context['upd_author_id'] = self.get_object().author.authorUser.id
        context['upd_is_author'] = context['upd_user_id'] == context['upd_author_id']
<<<<<<< HEAD
        context['upd_admin'] = self.request.user.is_superuser
=======
        context['author_name'] = str(*Author.objects.filter(authorUser_id=self.request.user.id)) if not self.request.user.is_superuser else f"Admin: <{self.request.user.username}>"
        context['author_list'] = list(Author.objects.all())

>>>>>>> dev
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

<<<<<<< HEAD
=======
# @login_required
# def update_me(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.group.filter(name='authors').exists():   #!!!!!!!!
#         authors_group.user_set.add(user)
#     return redirect('/news')

>>>>>>> dev
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





# class IndexView(View):
#     def get(self, request):
#         # printer.delay(10)
#         # printer.apply_async([10], countdown=5) # Параметр countdown устанавливает время (в секундах), через которое задача должна начать выполняться
#         printer.apply_async([10],
#                             eta = datetime.now() + timedelta(seconds=5)) # для реализации того же самого сдвига на 5 секунд мы можем получить текущее время и добавить timedelta, равное 5 секундам, чтобы получить datetime-объект момента через 5 секунд от текущего.
#         hello.delay()
#         return HttpResponse('Hello!')