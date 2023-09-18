from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=100,default='')
    email =  models.CharField(max_length=70)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=70)
    message = models.TextField()
    date = models.DateField()
    captcha = models.CharField(max_length=10,default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Frontend(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='school_logos/')
    ceo_name = models.CharField(max_length=200)
    ceo_image = models.ImageField(upload_to='ceo_images/')
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=20,default='')
    address = models.CharField(max_length=200)
    hero_image = models.ImageField(upload_to='hero_images/')
    hero_image_title = models.CharField(max_length=200,default='')
    intro = models.FileField(upload_to='intro', blank=True, null=True)
    about_image1 = models.ImageField(upload_to='about_images/')
    about_image2 = models.ImageField(upload_to='about_images/')
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, blank=True, null=True)
    instagram_url = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        get_latest_by = 'id'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
  

    def __str__(self):
        return self.name




class ParentHelp(models.Model):
    # Fields for parent information
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField(max_length=100)
    parent_phone = models.CharField(max_length=20)

    # Fields for child information
    child_name = models.CharField(max_length=100)
    child_dob = models.DateField()
    child_grade = models.IntegerField()
    child_school = models.CharField(max_length=100)

    # Additional fields for admission assistance
    admission_type = models.CharField(max_length=100)
    admission_deadline = models.DateField()
   

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parent_name}'s request for {self.child_name}'s admission assistance"



class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    slug = models.SlugField(unique=True, max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title        