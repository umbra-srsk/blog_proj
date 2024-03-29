"""myboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('insertform/', views.insert_form, name='insert'),
    #path('insertres/', views.insert_res),
    path('insert/', views.insert_proc, name='insert'),
    path('detail/<int:id>', views.detail, name='detail'),
    #path('updateform/<int:id>', views.update_form, name='update'),
    #path('updateres/',views.update_res),
    path('update/<int:id>', views.update_proc, name='update'),
    path('delete/<int:id>', views.delete_proc, name='delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('weather/', views.weather, name = 'weather'),
    #path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('add_reply/', views.add_reply, name='add_reply'),
    path('get_replies/<int:id>/', views.get_replies, name='get_replies'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('result/', views.result, name = 'result'),
    path('posts/', views.PostListView.as_view(), name ='post_list'),

]

