from django.db import models
from django.utils.text import slugify
from BackEnd.models import CustomUser
from FrontEnd.models import Category
from django.core.validators import FileExtensionValidator

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    def get_popular_posts(self, num_posts):
        """
        Returns the most popular blog posts based on the views count.
        The number of popular posts to return is specified by num_posts.
        """
        popular_posts = Blog.objects.filter(views_count__gt=0).order_by('-views_count')[:num_posts]
        return popular_posts


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def num_likes(self):
        return self.like_set.count()    

    def num_comment(self):    
        return self.comment_set.count()
        
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField(max_length=100)
    body = models.TextField()
    def __str__(self):
        return self.sender_name
    
class Image(models.Model):
    title = models.CharField(max_length=200)
    media_file = models.FileField(upload_to='Blog_media/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_images')
    def __str__(self):
        return self.title
