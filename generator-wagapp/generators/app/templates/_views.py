from django.contrib.syndication.views import Feed
from .models import <%= pagenamecamel %>IndexPage, <%= pagenamecamel %>Page, Category<%= pagenamecamel %>Page
from django.shortcuts import get_object_or_404, render


def tag_view(request, tag):
    index = <%= pagenamecamel %>IndexPage.objects.first()
    return index.serve(request, tag=tag)


def category_view(request, category):
    index = <%= pagenamecamel %>IndexPage.objects.first()
    return index.serve(request, category=category)


def author_view(request, author):
    index = <%= pagenamecamel %>IndexPage.objects.first()
    return index.serve(request, author=author)