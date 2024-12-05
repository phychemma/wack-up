from django import forms
from .models import Comment
class SearchForm(forms.Form):
  wg= forms.TextInput(attrs={"class":"form-control form-control-success text-success"})
  search_post = forms.CharField(widget=wg)
  
  
class EmailPostForm(forms.Form):
  wg= forms.TextInput(attrs={"class":"form-control form-control-success text-success"})
  name= forms.CharField(max_length=25,widget=wg)
  email= forms.EmailField(widget=wg)
  to= forms.EmailField(widget=wg)
  comment= forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control w-75 mx-auto text-success"}))
class CommentForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    fields_user= ['name', 'email', 'body']
    for field in fields_user:
       self.fields[field].widget.attrs.update({'class':'form-control'})
    
  class Meta:
    model= Comment
    fields= ['name', 'email', 'body']