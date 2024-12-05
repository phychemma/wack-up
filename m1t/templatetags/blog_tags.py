from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()

@register.simple_tag
def total_count():
  return Post.objects.count()

@register.inclusion_tag("m1t/post/ht_tag/latest_posts.html")
def show_latest_posts(count=5):
  latest_post=Post.objects.order_by('-publish')[:count]
  return {"latest_posts" : latest_post}
  
@register.inclusion_tag("m1t/post/ht_tag/most_commented_post.html")
def most_comment(count=5):
  most_commented_post= Post.objects.annotate(comment_count= Count('comment')).order_by('-comment_count')[:count]
  return {"most_commented_post":most_commented_post}
  
@register.filter(name= 'markdown')
def markdown_format(text):
  return mark_safe(markdown.markdown(text))