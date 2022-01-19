from django.urls import path
from Account_App import views


app_name = 'Account_App'

urlpatterns = [
     path('signup', views.sign_up, name='sign_up'),
     path('signin',views.sign_in, name='sign_in'),
     path('signout',views.sign_out,name='sign_out'),
     path('edit',views.edit_profile, name = 'edit_profile'),
     path('profile',views.profile, name= 'profile'),
     path('user/<username>',views.user_view, name= 'user'),
     path('follow/<username>',views.follow,name='follow'),
     path('unfollow/<username>',views.unfollow,name='unfollow'),

]