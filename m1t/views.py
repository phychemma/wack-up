from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import Http404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector ,SearchQuery,SearchRank , TrigramSimilarity
# Create your views here.
from .models import Post, Comment
from . import forms
class PostListView(ListView):
  model= Post
  #.objects.all()
  context_object__name= "posts"
  paginate_by= 3
  template_name= 'm1t/post/posts.html'
  
def post_list(req, tag_slug=None):
  all_post= Post.objects.all()
  tag=None
  if tag_slug:
    tag= get_object_or_404(Tag, slug= tag_slug)
    all_post= all_post.filter(tags__in=[tag])
  paginator=Paginator(all_post, 3)
  page_number= req.GET.get('page', 1)
  try:
    posts= paginator.page(page_number)
  except PageNotAnInteger:
    posts= paginator.page(1)
  except EmptyPage:
    posts= paginator.page(paginator.num_pages)
  return render(req, 'm1t/post/posts.html', {'posts':posts, 'tag' : tag })


def post_details(req, year, month, day, post):
  post = get_object_or_404(Post,
  status=Post.Status.DRAFT,
  publish__year=year,
  publish__month=month,
  publish__day=day,
  slug=post
  )
  form= forms.CommentForm()
  comments= post.comment.filter(active=True)
  post_tags_ids= post.tags.values_list('id', flat=True)
  similar_posts= Post.objects.filter(tags__in= post_tags_ids).exclude(id= post.id).annotate(same_tags= Count('tags')).order_by("-same_tags", "-publish")[:4]
 # try:
 #    post = Post.objects.get(id=id)
 # except Post.DoesNotExist
 #    raise Http404("Post not found")
  return render(req, "m1t/post/details.html", {'post':post,'comments':comments, 'form':form, 'similar_posts': similar_posts})
def share_post(req, id):
  post= get_object_or_404(Post, id=id, status= Post.Status.DRAFT)
  sent= False
  form= forms.EmailPostForm()
  if req.method == 'POST' :
    form =forms.EmailPostForm(req.POST)
    if form.is_valid():
      cd= form.cleaned_data
      url= req.build_absolute_uri(post.get_absolute_url())
      subject= f"{cd['name']} recommended you to view {post.title}"
      message= f"Read {post.title} at {url} \n Here was {cd['name']} comment \n {cd['comment']}"
      send_mail(subject, message, "phychemma4@gmail.com",[cd['to']])
      sent= True
  else:
    form= forms.EmailPostForm()
  return render(req, 'm1t/post/share.html', {'post':post,  'form': form, 'sent':sent})
@require_POST
def post_comment(req, post_id):
  post = get_object_or_404(Post, id= post_id, status= Post.Status.DRAFT )
  comment=None
  form = forms.CommentForm(req.POST)
  if form.is_valid :
    comment= form.save(commit= False)
    comment.post=post
    comment.save()
  return render(req, "m1t/post/comment.html", {'post':post, 'comment':comment, 'form': form })
def post_search(req):
  form= forms.SearchForm()
  query= None
  result = []
  if 'search_post' in req.GET:
    form = forms.SearchForm(req.GET)
    if form.is_valid():
      query = form.cleaned_data['search_post']
      #search_query= SearchQuery(query)
     # search_vector=SearchVector('title', weight='A') + SearchVector('body', weight='B')
      result= Post.objects.annotate(
        similarities= TrigramSimilarity('title', query)
      #  search= search_vector,
    #    rank= SearchRank(search_vector, search_query)
        ).filter(similarities__gt=0.1).order_by('-similarities')
  return render(req, 'm1t/post/postsearch.html', {'form':form,'query':query, 'result':result})
    