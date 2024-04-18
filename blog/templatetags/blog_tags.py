from django import template
from ..models import Post , Comment
from django.db.models import Count , Min , Max
from markdown import markdown


register = template.Library()

@register.simple_tag
def total_post():
    return Post.published.count()

@register.simple_tag
def total_comment():
    return Comment.objects.filter(active = True).count()


@register.simple_tag
def favirate_post(count=5):
    return Post.published.annotate(comment_count = Count('comments')).order_by('-comment_count')[:count]

@register.simple_tag
def min_post():
    return Post.published.aggregate(Max('reading_time'))


@register.inclusion_tag("partials/latest_post.html")
def latest_post(count=4):
    l_post = Post.published.order_by('-publish')[:count]
    context ={
        "l_post":l_post
    }
    return context