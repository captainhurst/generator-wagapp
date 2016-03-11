from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap

import <%= pagenamelower %>_page.views as <%= pagenamelower %>

urlpatterns = [
  
  url(r'^<%= slug %>/tag/(?P<tag>[-\w]+)/', <%= pagenamelower %>.tag_view, name="tag"),
  url(r'^<%= slug %>/category/(?P<category>[-\w]+)/', <%= pagenamelower %>.category_view, name="category"),
  url(r'^<%= slug %>/author/(?P<author>[-\w]+)/', <%= pagenamelower %>.author_view, name="author"),

]


    