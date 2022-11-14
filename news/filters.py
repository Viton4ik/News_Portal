


from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, DateFromToRangeFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Author, Category
from django.forms import DateInput
from django import forms


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):

    topic = CharFilter(field_name='topic',
                       lookup_expr='contains',
                       label='Topic:')

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author:',
        empty_label='any',
    )


    postCategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category:',
        empty_label='any',
    )

    # add time widget
    createTime_filer = DateTimeFilter(
        field_name='createTime',
        lookup_expr='gte',
        label='Creation date:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}, #attrs={'type': 'date'},
        ),
    )

    class Meta:
       model = Post
       fields = {

       }

