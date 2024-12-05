import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
  title = 'My blog'
  link = reverse_lazy('m1t:post_list')
  describtion = "New Post Of Blog"
  def items(self):
    return Post.objects.all()[:2]
  def item_title(self, item):
    return item.title
  def item_description(self, item):
    return truncatewords_html(markdown.markdown(item.body), 30)
  def item_pubdate(self, item):
    return item.publish