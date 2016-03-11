from django.contrib.syndication.views import Feed
from .models import GenericIndexPage, GenericPage, CategoryGenericPage
from django.shortcuts import get_object_or_404, render


def tag_view(request, tag):
    index = GenericIndexPage.objects.first()
    print("Index", index)
    return index.serve(request, tag=tag)


def category_view(request, category):
    index = GenericIndexPage.objects.first()
    return index.serve(request, category=category)


def author_view(request, author):
    index = GenericIndexPage.objects.first()
    return index.serve(request, author=author)