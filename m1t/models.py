from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.
class U0_a246(models.Manager):
   def get_query(self):
      return super().get_query().filter(author__username="u0_a246")
class Post(models.Model):
   class Status(models.TextChoices):
      DRAFT= 'DF', 'DRAFT'
      PUBLISHED= 'PB', 'Published' 
   tags= TaggableManager()
   title = models.CharField(max_length=250)
   slug  = models.SlugField(max_length=250, unique_for_date="publish")
   body  = models.TextField()
   publish= models.DateTimeField(default=timezone.now)
   created= models.DateTimeField(auto_now_add=True)
   updated= models.DateTimeField(auto_now=True)
   status = models.CharField(max_length=2, choices= Status.choices, default= Status.DRAFT)
   author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="blog_post" )
   objects= models.Manager()
   u0_a246=U0_a246()
   class Meta:
     ordering= ["-publish"]
     indexes =[
	  models.Index(fields= ["-publish"]),
	]
   def __str__(self):
      return self.title
   def get_absolute_url(self):
	   return reverse("m1t:post_details", args=[self.publish.year, self.publish.month, self.publish.day, self.slug,])
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comment')
  email= models.EmailField()
  name= models.CharField(max_length=80)
  body= models.TextField()
  created= models.DateTimeField(auto_now_add=True)
  updated= models.DateTimeField(auto_now=True)
  active= models.BooleanField(default= True)
  class Meta:
    ordering= ['created']
    indexes= [
      models.Index(fields=["created"])
      ]
  def __str__(self):
    return f"{self.name} comment on {self.post}"