
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# from news.resources import CONTENT_TYPE


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    authorRating = models.SmallIntegerField(default=0)

    # обновляет рейтинг пользователя, переданный в аргумент этого метода. состоит из следующего:
    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям автора.
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
    #     print(postRat, pRat)
        pRat += postRat.get('postRating')

        # суммарный рейтинг всех комментариев автора;
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
    #     print(commentRat, cRat)
        cRat += commentRat.get('commentRating')

        # суммарный рейтинг каждой статьи автора умножается на 3;
        self.authorRating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    news = 'news'
    post = 'post'
    CONTENT_TYPE = [
        (news, 'новость'),
        (post, 'статья'),
    ]
    # поле с выбором — «статья» или «новость»;
    contentType = models.CharField(max_length=4, choices=CONTENT_TYPE, default=post)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True)
    # заголовок статьи / новости;
    topic = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        return f"{self.content[0:123]}..."

    def __str__(self):
        return f'{self.topic.title()}: {self.content[:20]}... Created: {self.createTime}\n'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.postThrough.content[:64]}...'

class Comment(models.Model):
    text = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'