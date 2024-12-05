from django.urls import path
from .feeds import LatestPostsFeed
from . import views
app_name="m1t"


urlpatterns= [
  path('',views.post_list, name='post_list'),
#  path('',views.PostListView.as_view() ,name='post_list'),
path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
  path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_details,name='post_details'),
  path('<int:id>/share', views.share_post, name='share_post'),
  path('<int:post_id>/comment', views.post_comment,name='post_comment'),
  path('feeds/', LatestPostsFeed(), name='post_feeds'),
  path('searchpost/', views.post_search, name= 'search_post')
]
