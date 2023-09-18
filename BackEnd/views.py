from django.shortcuts import render , redirect ,HttpResponse
from django.contrib.auth import authenticate , login as auth_log
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import update_session_auth_hash

# Create your views here.
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
               return redirect('staff_home')
            elif user_type == '3':
               return redirect('guest_home')
            elif user_type == '4':
                return redirect('t_home')
            
        else:
            messages.error(request,' Username and password is incorrect ! please try right Credentials ')
            return redirect('login')  
            
              
    data={
        'title':"|| Get In Main Page ||"
    }
    return render(request,"login.html",data)   
    
@login_required(login_url='login/hod')
def HOD_HOME(request):
    return render (request,'HOD/home.html')
        

@login_required(login_url='login') 
def editprofile(request):
        user = CustomUser.objects.get(id = request.user.id)
        if request.method == "POST":
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bio = request.POST.get('bio')
            # print(profile_pic)
            email = request.POST.get('email')
            username = request.POST.get('username')
            try:
                customuser = CustomUser.objects.get(id = request.user.id)
                customuser.first_name = first_name
                customuser.username = username
                customuser.email = email
                customuser.last_name = last_name
                customuser.bio = bio
               
                if profile_pic != None and profile_pic != '':
                     customuser.profile_pic = profile_pic
                customuser.save()
                return redirect('profile')
                messages.success(request,'Profile Update')

            except:
                messages.error(request,'Faild To Update Your Profile')
                return redirect('editprofile')
        data = {
                'user':user,
                
            }
        return render(request,'BACKEND/editprofile.html',data)   

@login_required(login_url='login')    
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    # Check if the request method is POST
    if request.method == "POST":
        # Get the old password from the POST request
        oldpass = request.POST.get("oldpass")
        # Get the new password from the POST request
        newpass = request.POST.get("newpass")
        # Get the confirm password from the POST request
        confirmpass = request.POST.get("confirmpass")

        # Check if the old password is correct
        if check_password(oldpass, user.password):
            # Check if the new password and confirm password match
            if newpass == confirmpass:
                # Update the user's password
                user.password = make_password(newpass)
                user.save()

                # Update the session authentication hash to prevent logout
                update_session_auth_hash(request, user)

    data = {
        "user": user,
    }

    return render(request, "BACKEND/profile.html", data)


    
@login_required(login_url='login')
def events(request):
    return render (request,'BACKEND/Event.html')

    
@login_required(login_url='login')
def inbox(request):
    return render (request,'BACKEND/inbox.html')

    
@login_required(login_url='login')
def compose(request):
    return render (request,'BACKEND/compose.html')