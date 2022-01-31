from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateNewUser, EditProfile, SigninForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse,reverse_lazy
from .models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from Post_App.forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import messages


def sign_up(request):
     my_form = CreateNewUser()
     registerd = False

     if request.method == 'POST':
          my_form = CreateNewUser(data=request.POST)
          if my_form.is_valid():
               user = my_form.save()
               registerd = True
               try:
                    user_profile = UserProfile(user=user)
                    user_profile.save()
                    messages.success(request,"Yor account has been created.")
                    return HttpResponseRedirect(reverse('Account_App:sign_in'))
               except:
                    messages.warning(request,"There is a problem creting in your accont. Please check and try again!")
               return HttpResponseRedirect(reverse('Account_App:sign_in'))

     return render(request,'Account_App/signup.html',context={'title':'PhotoGram | Signup','form':my_form,'registerd':registerd})

def sign_in(request):
     form = SigninForm()
     if request.method == "POST":
          form = SigninForm(data=request.POST)
          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username,password=password)
               if user is not None:
                    login(request,user)
                    return HttpResponseRedirect(reverse('Post_App:home_page'))
               
     return render(request,'Account_App/signin.html',context={'title':'Signin Your Account','form':form})

@login_required
def sign_out(request):
     logout(request)
     return HttpResponseRedirect(reverse('Account_App:sign_in'))

@login_required
def edit_profile(request):
     current_user = UserProfile.objects.get(user=request.user )
     form = EditProfile(instance = current_user)

     if request.method == "POST":
          form = EditProfile(request.POST, request.FILES, instance = current_user)
          if form.is_valid():
               form.save(commit=True)
               form = EditProfile(instance=current_user)
               return HttpResponseRedirect(reverse('Account_App:profile'))

     return render(request,'Account_App/edit_profile.html',context={'form':form, 'title':'Edit Profile'})
@login_required
def profile(request):

     form = PostForm()
     comment_form = CommentForm()

     if request.method == "POST":
          form = PostForm(request.POST, request.FILES)

          if form.is_valid():

               post = form.save(commit=False)
               post.author = request.user
               post.save()

               return HttpResponseRedirect(reverse('Account_App:profile'))
     return render (request,'Account_App/profile.html',context={'form':form,'comment_form':comment_form})


@login_required
def user_view(request,username):
     other_user = User.objects.get(username=username)
     already_followed = Follow.objects.filter(follower = request.user, following= other_user )

     comment_form = CommentForm()
     if other_user == request.user:
          return HttpResponseRedirect(reverse('Account_App:profile'))
     return render(request,'Account_App/user.html',context={'other_user':other_user,'followed':already_followed, 'comment_form':comment_form })



@login_required
def follow(request,username):
     following_user = User.objects.get(username=username)
     follower_user = request.user

     already_followed = Follow.objects.filter(follower = follower_user, following= following_user )

     if not already_followed:
          followed_user = Follow(follower = follower_user,following = following_user)
          followed_user.save()
     return HttpResponseRedirect(reverse('Account_App:user',kwargs={'username':username}))


@login_required
def unfollow(request,username):
     following_user = User.objects.get(username=username)
     follower_user = request.user
     already_followed = Follow.objects.filter(follower = follower_user, following= following_user )
     already_followed.delete()
     return HttpResponseRedirect(reverse('Account_App:user',kwargs={'username':username}))

