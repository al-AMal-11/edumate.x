from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<str:slugs>/', views.blog_detail, name='blog_detail'),
    path('<str:slugs>/like/blog', views.like_blog, name='blog_like'),
    path('<str:slugs>/unlike/blog', views.unlike_blog, name='blog_unlike'),
    
    path('<str:slugs>/comment_text', views.coment_save, name='blog_comment_save')
    
]
