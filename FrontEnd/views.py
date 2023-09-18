from django.shortcuts import render ,redirect
from FrontEnd.models import Contact
from django.contrib.auth import authenticate , logout , login as auth_log
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from BackEnd.models import *
from Blogs.models import Blog
from . models import *
from typing import List, Dict
# Create your views here.
def get_frontend_data() -> List[Dict[str, any]]:
    frontend_data = []
    font = Frontend.objects.latest('id')

    frontend_data.append({
        'name': font.name,
        'logo': font.logo.url,
        'ceo_name': font.ceo_name,
        'ceo_image': font.ceo_image.url,
        'contact_email': font.contact_email,
        'phone_number': font.phone_number,
        'telephone_number': font.telephone_number,
        'address': font.address,
        'hero_image': font.hero_image.url,
        'hero_image_title': font.hero_image_title,
        'intro': font.intro.url if font.intro else '',
        'about_image1': font.about_image1.url,
        'about_image2': font.about_image2.url,
        'facebook_url': font.facebook_url,
        'twitter_url': font.twitter_url,
        'instagram_url': font.instagram_url,
        'linkedin_url': font.linkedin_url,
    })

    return frontend_data


   

def home(request):
    blogs = Blog.objects.all()[::-1][:10]
    new = News.objects.all() [::-1][:4]
    teacher = Teacher.objects.all()[::-1][:4]
    font = get_frontend_data()
    data = {
        'blogs':blogs,
        'new':new,
        'teacher':teacher,
        'font':font,
    }
    return render(request,'FontEND/home.html',data)

def about(request):
    new = News.objects.all() [::-1][:4]
    font = get_frontend_data()
    data = {
        'font':font,
         
        'new':new

    }
    return render(request,'FontEND/about.html',data)
def contacts(request):
    new = News.objects.all() [::-1][:4]
    font = get_frontend_data()
    data = {
       
        'new':new,
        'font':font,
        
    }
    return render(request,'FontEND/contacts.html',data)       
def contact_form(request):
    if request.method == 'POST':
        # retrieve the data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        message = request.POST.get('message')
        captcha = request.POST.get('captcha')

        # create a new ContactForm object and save it to the database
        contact_form = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date = datetime.date.today(),
            message=message,
            captcha=captcha
        )
        contact_form.save()

        # redirect the user to a thank you page
        return redirect('contacts_page')
# end contacts    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = authenticate(username=username , password=password)
        if users is not None:
            # login(cheackuser)
            auth_log(request,users)
          
            user_type = users.user_type
            if user_type == '1':
                 return redirect('hod_home')
            elif user_type == '2':
                pass
            elif user_type == '3':
                pass
            
        else:
            messages.error(request,' Username and password is incorrect ! please try right Credentials ')
            return redirect('login')  
            
              
    data={
        'title':"|| Get In Main Page ||"
    }
    return render(request,"login.html",data)   
    





def dologout(request):
    logout(request)
    return redirect('login')

def request_admission_assistance(request):
    if request.method == 'POST':
        parent_name = request.POST['parent_name']
        parent_email = request.POST['parent_email']
        parent_phone = request.POST['parent_phone']
        child_name = request.POST['child_name']
        child_dob = request.POST['child_dob']
        child_grade = request.POST['child_grade']
        child_school = request.POST['child_school']
        admission_type = request.POST['admission_type']
        admission_deadline = request.POST['admission_deadline']
        

        new_request = ParentHelp.objects.create(
            parent_name=parent_name,
            parent_email=parent_email,
            parent_phone=parent_phone,
            child_name=child_name,
            child_dob=child_dob,
            child_grade=child_grade,
            child_school=child_school,
            admission_type=admission_type,
            admission_deadline=admission_deadline,
          
        )
        return redirect('admission')    
def admission(request):
    new = News.objects.all() [::-1][:4]
    font = get_frontend_data()
    data = {
       
        'new':new,
        'font':font,

    }
    return render(request,'FontEND/admision_post.html',data)



def news_r(request,news):
    new = News.objects.get(slug=news)
    font = get_frontend_data()
    recent = News.objects.all() [::-1][:4]
    data = {
        'news':new,
        'new':recent,
        'font':font,
        
    }
    return render(request,'FontEND/recent_news.html',data)