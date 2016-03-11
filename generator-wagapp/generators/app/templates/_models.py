from __future__ import unicode_literals

from django.db import models

from datetime import date

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render


from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from home.models import MainStreamBlock

# Create your models here.
def get_page_context(context):
    """ Get context data useful on all blog related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='<%= pagenamelower %>page'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    
    context['all_categories'] = <%= pagenamecamel %>Category.objects.all()
    
    context['root_categories'] = <%= pagenamecamel %>Category.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        page_count=Count('<%= pagenamelower %>page'),
    )
    return context


class <%= pagenamecamel %>IndexPage(Page):

  @property
  def <%= pagenamelower %>_pages(self):
      gp = <%= pagenamecamel %>Page.objects.descendant_of(self).live()
      gp = gp.order_by(
            'title'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )

      return gp

  def get_context(
                  self, 
                  request, 
                  tag=None, 
                  category=None, 
                  author=None, 
                  *args,
                  **kwargs
                  ):
        
        context = super(<%= pagenamecamel %>IndexPage, self).get_context(request, *args, **kwargs)
        
        gp = self.<%= pagenamelower %>_pages

        if tag is None:
            tag = request.GET.get('tags')

        if tag:
            gp = gp.filter(tags__slug=tag)
        
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    Category<%= pagenamecamel %>Page, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(<%= pagenamecamel %>Page, slug=category)
            gp = gp.filter(categories__category__name=category)
        
        if author:
            if isinstance(author, str) and not author.isdigit():
                gp = gp.filter(author__username=author)
            else:
                gp = gp.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = 20

        if page is not None:
            
            paginator = Paginator(page, page_size)  # Show 20 <%= pagenamecamel %> Pages per page

            try:
                gp = paginator.page(page)
            except PageNotAnInteger:
                print(page)
                gp = paginator.page(1)
            except EmptyPage:
                gp = paginator.page(paginator.num_pages)

        context['page'] = gp
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context = get_page_context(context)
        print("Context:", context)

        return context

  class Meta:
    verbose_name = _('<%= pagenamecamel %> Page Index')
  
  subpage_types = ['<%= pagenamelower %>_page.<%= pagenamecamel %>Page']


class <%= pagenamecamel %>PageTag(TaggedItemBase):
    content_object = ParentalKey('<%= pagenamelower %>_page.<%= pagenamecamel %>Page', related_name='tagged_items')

@register_snippet
class <%= pagenamecamel %>Category(models.Model):
    name = models.CharField(
                            max_length=80,
                            unique=True, 
                            verbose_name=_('Category Name')
                          )
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.')
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Page Category")
        verbose_name_plural = _("Page Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(<%= pagenamecamel %>Category, self).save(*args, **kwargs)

class Category<%= pagenamecamel %>Page(models.Model):
    category = models.ForeignKey(
                                  <%= pagenamecamel %>Category, 
                                  related_name="+", 
                                  verbose_name=_('Category')
                                )
    page = ParentalKey('<%= pagenamecamel %>Page', related_name='categories')
    
    panels = [
        FieldPanel('category'),
    ]

limit_author_choices = {'is_staff': True}

class <%= pagenamecamel %>Page(Page):
  tags          = ClusterTaggableManager(through=<%= pagenamecamel %>PageTag, blank=True)
  body          = StreamField(MainStreamBlock())
  search_fields = Page.search_fields + (
    index.SearchField('body'),
  )
  page_categores = models.ManyToManyField(
        <%= pagenamecamel %>Category, through=Category<%= pagenamecamel %>Page, blank=True
        )
  author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, 
        null=True,
        limit_choices_to=limit_author_choices,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )
  
  class Meta:
    verbose_name = "Standard Page"

<%= pagenamecamel %>Page.content_panels = [
  FieldPanel('title', classname="full title"),
  MultiFieldPanel([
        FieldPanel('tags'),
        InlinePanel('categories', label=_("Categories")),
    ], heading="Tags and Categories"),
  StreamFieldPanel('body'),
]

<%= pagenamecamel %>Page.promote_panels = Page.promote_panels
