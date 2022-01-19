from django.urls import path
from . import views


app_name = 'Post_App'

urlpatterns = [
     path('',views.home,name='home_page'),
     path('like/<pk>/',views.liked ,name='like'),
     path('unlike/<pk>/',views.unliked,name='unlike')
]