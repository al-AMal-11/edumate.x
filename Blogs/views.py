from django.shortcuts import render, get_object_or_404 ,redirect
from django.db.models import F ,Value
from .models import *
from django.db.models import Count
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from FrontEnd.views import get_frontend_data
from django.contrib import admin
from FrontEnd.models import  *
# Create your views here.
def blogs(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('search')
    
    if search_query:
        blogs = Blog.objects.filter(title__icontains=search_query).order_by('-published_date')
    elif category_filter and tag_filter:
        blogs = Blog.objects.filter(category__name=category_filter, tags__name=tag_filter).order_by('-published_date')
    elif category_filter:
        blogs = Blog.objects.filter(category__name=category_filter).order_by('-published_date')
    elif tag_filter:
        blogs = Blog.objects.filter(tags__name=tag_filter).order_by('-published_date')
    else:
        blogs = Blog.objects.all().order_by('-published_date')

    blog_list = []
    for blog in blogs:
        blog_dict = {
            'title': blog.title,
            'body': blog.body,
            'author': blog.author,
            'published_date': blog.published_date,
            'categories': blog.category,
            'tags': blog.tags.all(),
            'image': blog.image,
            'video': blog.video,
            'slug': blog.slug,
            'views_count': blog.views_count,
        }
        blog_list.append(blog_dict)

    detail = Frontend.objects.all()
    font = get_frontend_data()
    new = News.objects.all() [::-1][:4]
    context = {
        'title': '|| ReadMore LearnMore',
        'detail': detail,
        'blog_list': blog_list,
        'font':font,

        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'new':new,
    }

    return render(request, 'BlogsApp/blog_list.html', context)

def blog_detail(request, slugs):
    # Retrieve single blog post based on slug
    
    blog = Blog.objects.get(slug=slugs)
    # Increment the view count for the blog post
    comments = blog.comment_set.all()
    my_images = blog.blog_images.all()
    detail = Frontend.objects.all()
    section = Category.objects.all()
    new = News.objects.all() [::-1][:4]
    font = get_frontend_data()
    tag = Tag.objects.all()

    if request.method == 'POST':
        sender_name = request.POST['author']
        sender_email = request.POST['email']
        body = request.POST['comment']
        comment = Comment(blog=blog, sender_name=sender_name, sender_email=sender_email, body=body)
        comment.save()

    blog.views_count += 1
    blog.save()

    context = {
        'blog': blog,
        'detail': detail,
        'title': blog.title,
        'section': section,
        'font':font,
        'tag': tag,
        'my_images':my_images,
        'comments': comments,
        'new':new,
    }
   
    return render(request, 'BlogsApp/blog_detail.html', context)

def coment_save(request,slugs):
    blog = Blog.objects.get(slug=slugs)
    if request.method == 'POST':

        sender_name = request.POST['comment_name']
        sender_email = request.POST['comment_email']
        body = request.POST['comment_body']
        comment = Comment(blog=blog, sender_name=sender_name, sender_email=sender_email, body=body)
        comment.save()
        return redirect('blog_detail',slugs)

@login_required
def like_blog(request, slugs):
    blog = Blog.objects.get(slug=slugs)
    try:
        Like.objects.create(blog=blog, user=request.user)
    except IntegrityError:
        pass
    return redirect('blog_detail',slugs)
@login_required
def unlike_blog(request, slugs):
    blog = Blog.objects.get(slug=slugs)
    try:
        like = Like.objects.get(blog=blog, user=request.user)
        like.delete()
    except Like.DoesNotExist:
        pass
    return redirect('blog_detail',slugs)

