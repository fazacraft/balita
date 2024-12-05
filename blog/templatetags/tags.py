from django import template
from random import randint
from blog.models import Post, Category, Tag

register = template.Library()


@register.simple_tag
def get_popular_posts():
    return Post.objects.filter(is_published = True).order_by('-views_count')[:5]

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.simple_tag
def get_lastest_posts():
    return Post.objects.filter(is_published = True).order_by('-created_at')[:3]

@register.simple_tag
def get_tags():
    return Tag.objects.all()