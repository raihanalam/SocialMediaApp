from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
     class Meta:
          model = Post
          fields = ['image','caption',]

class CommentForm(forms.ModelForm):
     comment = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'write your comment here...','style':'height:40px; padding-right:80px; ' }))
     class Meta:
          model = Comment
          fields = ['comment',]

