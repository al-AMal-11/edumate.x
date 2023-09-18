import queue
import quopri
from sqlite3 import IntegrityError
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from datetime import datetime
from FrontEnd.models import Frontend , Category ,Contact, ParentHelp , News
from .forms import ClassSelectForm
import datetime
from django.db.models import Sum
from decimal import Decimal
from django.db.models import Count , Q
from Blogs.models import Blog , Tag , Image
from django.utils.text import slugify
from datetime import date
from django.db.models import Sum, Avg
from statistics import mean
import os
import shutil
from PIL import Image as PILImage
from io import BytesIO

import pandas as pd
import tempfile
from django.http import HttpResponse
from django.apps import apps
import pytz  # Required for timezone conversion
from django.utils import timezone
from django.db.models import F
from django.db import models
from django.db.models import DateTimeField
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_naive
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from django.utils.timezone import make_naive
from openpyxl.utils.datetime import to_excel
import numpy as np
# ...
def convert_to_naive_datetime(dt):
    """
    Convert the given datetime to a naive datetime object.
    """
    if isinstance(dt, str):
        dt = parse_datetime(dt)
    if timezone.is_aware(dt):
        dt = make_naive(dt)
    return dt



def backup_data(request):
    # List of app names
    app_names = ['BackEnd', 'Blogs', 'FrontEnd']

    try:
        # Create a temporary directory to store the backup files
        temp_dir = tempfile.mkdtemp()

        # Iterate over each app
        for app_name in app_names:
            # Get a list of all models within the app
            app_models = apps.get_app_config(app_name).get_models()

            # Iterate over each model
            for model in app_models:
                # Retrieve all data from the model
                all_data = model.objects.all()

                # Convert datetime fields to timezone-unaware format
                for field in all_data.model._meta.fields:
                    if isinstance(field, DateTimeField) and field.name not in ['last_login', 'date_joined']:
                        field_name = field.name
                        all_data = all_data.annotate(
                            **{field_name: make_naive(field_name)})

                # Convert data to a pandas DataFrame
                data_frame = pd.DataFrame.from_records(all_data.values())

                # Convert datetime columns to timezone-unaware format
                for column in data_frame.select_dtypes(include='datetime64[ns]'):
                    data_frame[column] = data_frame[column].apply(make_naive)

                # Create an Excel workbook
                workbook = openpyxl.Workbook()
                sheet = workbook.active

                # Write the DataFrame to the sheet
                for row in dataframe_to_rows(data_frame, index=False, header=True):
                    sheet.append(row)

                # Save the workbook to an Excel file
                excel_file = os.path.join(temp_dir, f'{app_name}_{model.__name__}.xlsx')
                workbook.save(excel_file)

        # Specify the backup folder path relative to the "Downloads" folder
        backup_folder = os.path.join(os.path.expanduser("~"), 'Downloads', 'Backup')

        # Create the backup folder if it doesn't exist
        os.makedirs(backup_folder, exist_ok=True)

        # Move the backup files from the temporary directory to the backup folder
        shutil.move(temp_dir, backup_folder)

        # Compress the backup folder into a zip file
        zip_filepath = shutil.make_archive(backup_folder, 'zip', backup_folder)

        # Serve the zip file for download
        with open(zip_filepath, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=backup.zip'
            return response
    finally:
        # Cleanup: Remove the temporary directory
        shutil.rmtree(temp_dir)
@login_required(login_url='login')
def HOD_HOME(request):
   
    # Pylint(E1101:no-member)
    #Pylint(E1101:no-member)
    student_count = student.objects.all().count()
    staff_count = Teacher.objects.all().count()
    student_gender_male = student.objects.filter(student_gender='Male').count()
    student_gender_female = student.objects.filter(student_gender='Female').count()
    remaining_fees = Fees.objects.filter(payed=False)
    total_remaining_fees = remaining_fees.aggregate(Sum('amount'))['amount__sum']
    remaining_salaries = Salarys.objects.filter(payed=False)
    total_remaining_salaries = remaining_salaries.aggregate(Sum('amount'))['amount__sum']

    data = {
        'student_count': student_count,
        'staff_count': staff_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
        'total_fees': total_remaining_fees,
        'total_salary': total_remaining_salaries,
        'request': request
        
    }

    return render(request, 'HOD/HOD_HOME.html', data)


@login_required(login_url='login')
def Meeting(request):
    # Pylint(E1101:no-member)
    meeting = Meetings.objects.all()
    data = {
        'meeting': meeting,
        'request': request
    }
    return render (request,'HOD/HOD_meetings.html',data)

@login_required(login_url='login')
def Meetings_add(request):
    if request.method == "POST":
         meeting_type = request.POST.get('meeting_type')
         meeting_name = request.POST.get('meeting_name')
         meeting_date = request.POST.get('meeting_date')
         if meeting_type == '3':
            metting_t = 3
         elif meeting_type == '1':
             metting_t = 1   
         else:
            metting_t = 2   
         metting = Meetings(
            Meetings_Type = metting_t,
            Meeting_Name = meeting_name,
            Meeting_Date = meeting_date,
         )
         metting.save()
         return redirect('hod_meetings')
    return render (request,'HOD/HOD_meetings_add.html')


@login_required(login_url='login')
def Meeting_edit(request ,id):
    meeting = Meetings.objects.get(id = id)
    data = {
        'meeting':meeting
    }
    return render (request,'HOD/hod_meeting_edit.html',data)


@login_required(login_url='login')    
def Meeting_updade(request):
         if request.method == "POST":
           meeting_type = request.POST.get('meeting_type')
           meeting_name = request.POST.get('meeting_name')
           meeting_date = request.POST.get('meeting_date')
           Sid = request.POST.get('id')

           Meeting = Meetings.objects.get(id = Sid)
           Meeting.Meeting_Name = meeting_name
           Meeting.Meetings_Type = meeting_type
           Meeting.Meeting_Date = meeting_date
           Meeting.save()
              
         return redirect('hod_meetings')

@login_required(login_url='login')
def Meeting_delete(request ,id):
    Meeting = Meetings.objects.get(id = id)
    Meeting.delete()
    
    return  redirect ('hod_meetings')

# start teacher section 
@login_required(login_url='login')
def Teachers(request):
    staff = Teacher.objects.all()
    if staff:		
     for i in staff:
        staff_id = i.admin.id
        salary = Employe.objects.get(employe = staff_id)
        data = {
            'staff':staff,
            'salary':salary,
            'request': request
        }
        return render (request,'HOD/Teacher.html',data)
    else:
     return render(request,'HOD/Teacher.html')
      
@login_required(login_url='login')
def Teacher_add(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('Number')
        gender = request.POST.get('gender')
        Qualification = request.POST.get('Qualification')
        Experience = request.POST.get('Experience')
        subjects = request.POST.get('subject')
        Sections = request.POST.get('section')
        
        Subjectss = Subject.objects.get(id = subjects)
        Sectionis = Section.objects.get(id =Sections)

        Sallery = request.POST.get('Sallery')
        CitizenCard = request.POST.get('CitizenCard')
        password = request.POST.get('password')
        username = request.POST.get('username')
        staff_photo = request.FILES.get('teacher_photo')

        address = request.POST.get('address')
        if CustomUser.objects.filter(username=username ).exists():
           messages.error(request,'')
           return redirect('hod_student_add')
        if CustomUser.objects.filter(email=email ).exists():
           messages.error(request,'')
           return redirect('hod_student_add')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                profile_pic = staff_photo,
                user_type = 4

            )    
            user.set_password(password)
            user.save()
            

            teacher = Teacher(
                admin = user,
                staff_gender = gender,
                staff_subject = Subjectss,
                class_Teacher = Sectionis,
                staff_mobile = phone,
                staff_Qualification = Qualification,
                staff_Experience = Experience,
                CitizenCard_Number = CitizenCard,
               
                staff_address = address,
                staff_photo = staff_photo
            )
            teacher.save()
            Employes = Employe(
                employe  = user,
                salary = Sallery
            )
            Employes.save()
            messages.success(request,'Teacher is Add')
            return redirect('hod_teacher')
        
    section = Section.objects.all()        
    subject  = Subject.objects.all()
    data = {
        'section':section,
        'subject':subject

    }    
    return render (request,'HOD/Teacher_add.html',data)

@login_required(login_url='login')
def Teacher_edit(request, id):
    teacher_instance = Teacher.objects.get(id=id)
    salary = Employe.objects.get(employe = teacher_instance.admin.id)
    teacher_dict = {
        'id': teacher_instance.admin.id,
        'username': teacher_instance.admin.username,
        'first_name': teacher_instance.admin.first_name,
        'last_name': teacher_instance.admin.last_name,
        'email': teacher_instance.admin.email,
        'staff_gender': teacher_instance.staff_gender,
        'staff_subject': teacher_instance.staff_subject.id,
        'class_Teacher': teacher_instance.class_Teacher.id,
        'staff_mobile': teacher_instance.staff_mobile,
        'staff_Qualification': teacher_instance.staff_Qualification,
        'staff_Experience': teacher_instance.staff_Experience,
        'CitizenCard_Number': teacher_instance.CitizenCard_Number,
        'staff_address': teacher_instance.staff_address,
        'staff_photo': teacher_instance.staff_photo,
        'created_at': teacher_instance.created_at,
        'updated_at': teacher_instance.updated_at,
    }
    sections = Section.objects.all()
    subjects = Subject.objects.all()

    data = {
        'teacher': teacher_dict,
        'section': sections,
        'subject': subjects,
        'salary':salary
    }

    return render(request, 'HOD/teacher_edit.html', data)


@login_required(login_url='login')
def Teacher_detail(request ,id):
    staff = Teacher.objects.filter(id = id)
    data = {
        'staff':staff
    }
    return render (request,'HOD/Teacher_detail.html',data)


@login_required(login_url='login')
def Teacher_delete(request ,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    
    return  redirect ('hod_teacher')    

@login_required(login_url='login')
def Teacher_update(request):
    if request.method == "POST":
         first_name = request.POST.get('first_name')
         Sid = request.POST.get('id')
         last_name = request.POST.get('last_name')
         email = request.POST.get('email')
         gender = request.POST.get('gender')
         Experience = request.POST.get('Experience')
         subjects = request.POST.get('subject')
         Sections = request.POST.get('section')
         Subjectss = Subject.objects.get(id = subjects)
         Sectionis = Section.objects.get(id =Sections)
         Qualification = request.POST.get('Qualification')
         Sallery= request.POST.get('Sallery')
         phone= request.POST.get('Number')
         username = request.POST.get('username')
         password= request.POST.get('password')
         CitizenCard = request.POST.get('CitizenCard')
         teacher_photo = request.FILES.get('teacher_photo')
         address = request.POST.get('address')
         
         user = CustomUser.objects.get(id = Sid)
         user.last_name = last_name
         user.first_name = first_name
         user.email = email
         user.username = username
         if password != None and password != '':
            user.set_password(password)

         
         user.save()
         staff = Teacher.objects.get(admin = Sid)
         staff.staff_gender = gender
         staff.staff_subject = Subjectss
         staff.class_Teacher = Sectionis
         staff.staff_mobile = phone
         staff.staff_Qualification = Qualification
         staff.staff_Experience = Experience
         staff.CitizenCard_Number = CitizenCard
         
         staff.staff_address = address
         if teacher_photo != None and teacher_photo != '':
            staff.staff_photo = teacher_photo
         staff.save()   
         
         slary = Employe.objects.get(employe = user)
         slary.salary = Sallery
         slary.save()

       

         messages.success(request,'Student are update')
        

    return redirect('hod_teacher')    
# end of teacher sectiuon    
# start studnet section 
@login_required(login_url='login')
def Student_edit(request, id):
    student_instance = student.objects.get(id=id)
    student_dict = {
        'id': student_instance.admin.id,
        'username': student_instance.admin.username,
        'first_name': student_instance.admin.first_name,
        'last_name': student_instance.admin.last_name,
        'email': student_instance.admin.email,
        'student_id': student_instance.student_id,
        'student_class': student_instance.student_class.Class_Name,
        'student_gender': student_instance.student_gender,
        'student_dob': student_instance.student_dob,
        'student_Religion': student_instance.student_Religion,
        'student_Joining_date': student_instance.student_Joining_date,
        'student_Section': student_instance.student_Section.Section_Name,
        'student_father_name': student_instance.student_father_name,
        'student_father_occupation': student_instance.student_father_occupation,
        'student_father_number': student_instance.student_father_number,
        'studen_present_address': student_instance.studen_present_address,
        'created_at': student_instance.created_at,
        'updated_at': student_instance.updated_at,
        'student_Feedback': student_instance.student_Feedback,
        'studen_permanent_addres': student_instance.studen_permanent_addres,
        'Student_photo': student_instance.Student_photo,
    }
    Classis = Class.objects.all()
    Sectionis = Section.objects.all()

    data = {
        'students': [student_dict],
        'Classis': Classis,
        'sectionis': Sectionis
    }

    return render(request, 'HOD/student_edit.html', data)



@login_required(login_url='login')
def Student(request):
    students = student.objects.all()
    data = {
        'students':students,
        'request': request
    }
    return render (request,'HOD/Students.html',data)

@login_required(login_url='login')
def Student_add(request):
    
    if request.method == "POST":
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         email = request.POST.get('email')
         gender = request.POST.get('gender')
         student_id = request.POST.get('student_id')
         student_DOB = request.POST.get('DOB')
         Classs = request.POST.get('Class')
         Religion= request.POST.get('Religion')
         username = request.POST.get('username')
         password= request.POST.get('password')
         Section1 = request.POST.get('Section')
         Student_photo = request.FILES.get('Student_photo')
         father_name = request.POST.get('father_name')
         father_occupation = request.POST.get('father_occupation')
         father_number= request.POST.get('father_number')
         present_address= request.POST.get('present_address')
         permanent_address= request.POST.get('permanent_address')
         if CustomUser.objects.filter(username=username ).exists():
           messages.error(request,'Username is exist')
           return redirect('hod_student_add')
         if CustomUser.objects.filter(email=email ).exists():
           messages.error(request,'Email is exist')
           return redirect('hod_student_add')
         else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                profile_pic = Student_photo,
                user_type = 3

            )    
            user.set_password(password)
            user.save()
            class_obj = Class.objects.get(Class_Name=Classs)
            filter_sections =  Section.objects.filter(Class_Name=class_obj , Section_Name=Section1)
            section_obj = filter_sections.first()

            students = student(
                admin = user,
                student_id = student_id,
                student_class = class_obj,
                student_gender = gender,
                student_dob = student_DOB,
                student_Religion = Religion,
                student_Section = section_obj,
                student_father_name = father_name,
                student_father_occupation = father_occupation,
                student_father_number = father_number,
                studen_present_address = present_address,
                studen_permanent_addres = permanent_address,
                # studen_Joining_Date = datetime.today(),
                Student_photo = Student_photo,
            )
            students.save()
            messages.success(request,'')
            
            return redirect('hod_student')
    
    
    Classis = Class.objects.all()
    Sectionis = Section.objects.all()

    data = {
            
            'Classis':Classis,
            'sectionis':Sectionis
        }    
    return render (request,'HOD/Students_add.html',data)
    


@login_required(login_url='login')
def Student_detail(request ,id):
    students = student.objects.filter(id = id)
    data = {
        'students':students
    }
    return render (request,'HOD/student_detail.html',data)



@login_required(login_url='login')
def Student_delete(request ,admin):
    students = CustomUser.objects.get(id = admin)
    students.delete()
    
    return  redirect ('hod_student')



@login_required(login_url='login')
def Student_update(request ):
    if request.method == "POST":
         first_name = request.POST.get('first_name')
         Sid = request.POST.get('id')
         last_name = request.POST.get('last_name')
         email = request.POST.get('email')
         gender = request.POST.get('gender')
         student_id = request.POST.get('student_id')
         student_DOB = request.POST.get('DOB')
         Classs = request.POST.get('Class')
         Religion= request.POST.get('Religion')
         username = request.POST.get('username')
         password= request.POST.get('password')
         Section1 = request.POST.get('Section')
         Student_photo = request.FILES.get('Student_photo')
         father_name = request.POST.get('father_name')
         father_occupation = request.POST.get('father_occupation')
         father_number= request.POST.get('father_number')
         present_address= request.POST.get('present_address')
         permanent_address= request.POST.get('permanent_address')
         user = CustomUser.objects.get(id = Sid)
         user.last_name = last_name
         user.first_name = first_name
         user.email = email
         user.username = username
         if password != None and password != '':
            user.set_password(password)

         
         user.save()

         students = student.objects.get(admin = Sid)
         class_obj = Class.objects.get(Class_Name=Classs)
         filter_sections =  Section.objects.filter(Class_Name=class_obj , Section_Name=Section1)
         section_obj = filter_sections.first()

         students.student_id = student_id
         students.student_gender = gender
         students.student_dob = student_DOB
         students.student_Religion = Religion
         students.student_Section = section_obj
         students.student_father_name = father_name
         students.student_father_occupation = father_occupation
         students.student_father_number = father_number
         students.studen_present_address = present_address
         students.studen_permanent_addres = permanent_address
         students.student_class = class_obj
         if Student_photo != None and Student_photo != '':
            students.staff_photo = Student_photo
         students.save()   

         messages.success(request,'Student are update')
    return redirect('hod_student')     


# end student section     





@login_required(login_url='login')
def HOD_HOME_fornt_edit(request, id):
    
        
        school_obj = Frontend.objects.get(id=id)
        context = {'detail': [school_obj]}

        return render(request, 'HOD/front_end_edit.html', context)

@login_required(login_url='login')
def  HOD_HOME_fornt(request):
     detail = Frontend.objects.all()
     data = {
        'detail':detail,
        'request': request
     }
     return render(request,'HOD/front_end.html',data)


@login_required(login_url='login')    
def  HOD_HOME_fornt_update(request):
      if request.method == 'POST':
        school_name = request.POST.get('school_name')
        founder_name = request.POST.get('founder_name')
        school_email = request.POST.get('school_email')
        phone_number = request.POST.get('phone_number')
        telephone_number = request.POST.get('telephone_number')
        hero_image_title = request.POST.get('hero_image_title')
        address = request.POST.get('address')
        facebook_url = request.POST.get('facebook_url')
        twitter_url = request.POST.get('twitter_url')
        instagram_url = request.POST.get('instagram_url')
        linkedin_url = request.POST.get('linkedin_url')
        school_id = request.POST.get('id')

        first_home_page_image = request.FILES.get('first_home_page_image')
        about_image1 = request.FILES.get('about_image1')
        about_image2 = request.FILES.get('about_image2')
        intro_video = request.FILES.get('intro_video')

        school_obj = Frontend.objects.get(name=school_id)
        school_obj.name = school_name
        school_obj.ceo_name = founder_name
        school_obj.contact_email = school_email
        school_obj.phone_number = phone_number
        school_obj.telephone_number = telephone_number
        school_obj.hero_image_title = hero_image_title
        school_obj.address = address
        school_obj.facebook_url = facebook_url
        school_obj.twitter_url = twitter_url
        school_obj.instagram_url = instagram_url
        school_obj.linkedin_url = linkedin_url
        if first_home_page_image:
            school_obj.first_home_page_image = first_home_page_image
        if about_image1:
            school_obj.about_image1 = about_image1
        if about_image2:
            school_obj.about_image2 = about_image2
        if intro_video:
            school_obj.intro_video = intro_video
        school_obj.save()

        return redirect('hod_home_front')


@login_required(login_url='login')
def  hod_notification(request):
      
     
      return render(request,'HOD/Hod_notification.html')


@login_required(login_url='login')      
def  hod_notification_teacher(request):
    staff = Teacher.objects.all()
    data = {
        'staff':staff
    }
         
     
    return render(request,'HOD/hod_notification_teacher.html',data)


@login_required(login_url='login')    
def  hod_notification_teacher_send(request):
    if request.method == 'POST':
        staff_iid = request.POST.get('staff_id')
        staff_mesage = request.POST.get('staff_message')

        staff = Teacher.objects.get(admin = staff_iid)
        save_notificatio  = Teacher_notification(
            staff_id = staff,
            Message = staff_mesage
        )
        save_notificatio.save()
        messages.success(request , 'Notification is send')

        return redirect ('hod_notification')



@login_required(login_url='login')      
def  hod_notification_staff(request):
    staff = Staffs.objects.all()
    data = {
        'staff':staff
    }
         
     
    return render(request,'HOD/hod_notification_staff.html',data)


@login_required(login_url='login')      
def  hod_notification_guest_send(request):
    if request.method == 'POST':
        student_iid = request.POST.get('student_id')
        student_mesage = request.POST.get('student_message')

        guest = student.objects.get(admin = student_iid)
        save_notificatio  = Guest_Notification(
            guest_id = guest,
            Message = student_mesage
        )
        save_notificatio.save()
        messages.success(request , 'Notification is send')          
     
        return redirect('hod_notification')

@login_required(login_url='login')    
def  hod_notification_staff_send(request):
    if request.method == 'POST':
        staff_iid = request.POST.get('staff_id')
        staff_mesage = request.POST.get('staff_message')

        staff = Staffs.objects.get(staff = staff_iid)
        save_notificatio  = Staff_notifica(
            staff_id = staff,
            Message = staff_mesage
        )
        save_notificatio.save()
        messages.success(request , 'Notification is send')

        return redirect ('hod_notification')



@login_required(login_url='login')     
def  hod_notification_guest(request):
    

        students = student.objects.all()
        data = {
        'students':students
        }

                           
     
        return render(request,'HOD/Hod_notification_guest.html',data)
                           
     

@login_required(login_url='login')     
def  hod_leave_views(request):
    student_leave = Student_leave.objects.filter(status = 0)[:10]
    staff_leave = Staff_leave.objects.filter(status = 0)[:10]
    teacher_leave = Teacher_leave.objects.filter(status = 0)[:10]

    data = {
        'student_leave': student_leave,
        'staff_leave':staff_leave,
        'teacher_leave':teacher_leave,
        'request': request
    }
    return render(request,'HOD/Hod_leave_views.html',data)
                           
     
@login_required(login_url='login')     
def hod_leave_views_staff_approve(request , status):
    leave = Staff_leave.objects.get(id=status)
    leave.status = 1
    leave.save()
    
    return redirect('hod_leave_views')
     
@login_required(login_url='login')     
def hod_leave_views_staff_disapprove(request , status):
    leave = Staff_leave.objects.get(id=status)
    leave.status = 2
    leave.save()
    
    return redirect('hod_leave_views')
     
@login_required(login_url='login')     
def hod_leave_views_student_approve(request , status):
    leave = Student_leave.objects.get(id=status)
    leave.status = 1
    leave.save()
    
    return redirect('hod_leave_views')
     
@login_required(login_url='login')     
def hod_leave_views_student_disapprove(request , status):
    leave = Student_leave.objects.get(id=status)
    leave.status = 2
    leave.save()
    
    return redirect('hod_leave_views')

@login_required(login_url='login')     
def hod_leave_views_teacher_approve(request , status):
    leave = Teacher_leave.objects.get(id=status)
    leave.status = 1
    leave.save()
    
    return redirect('hod_leave_views')
     
@login_required(login_url='login')     
def hod_leave_views_teacher_disapprove(request , status):
    leave = Teacher_leave.objects.get(id=status)
    leave.status = 2
    leave.save()
    
    return redirect('hod_leave_views')

@login_required(login_url='login')  
def hod_feedback(request):
    staff_feedback = Staff_Feedback.objects.all()[:10] [::-1]
    guest_feedback = Guest_Feedback.objects.all()[:10] [::-1]
    teacher_feedback = Teacher_Feedback.objects.all()[:10] [::-1]

    data = {
        'staff_feedback':staff_feedback,
        'guest_feedback':guest_feedback,
        'teacher_feedback':teacher_feedback,
        'request': request
    }
    return render(request,'HOD/hod_feedback.html',data)

@login_required(login_url='login') 
def hod_feedback_staff_reply(request):
    if request.method == "POST":
        Reply = request.POST.get('Reply')
        feedback_id = request.POST.get('id')
        feedback_is = Staff_Feedback.objects.get(id=feedback_id)
        feedback_is.feedback_reply = Reply
        feedback_is.save()

        return redirect('hod_feedback')

@login_required(login_url='login') 
def hod_feedback_teacher_reply(request):
    if request.method == "POST":
        Reply = request.POST.get('Reply')
        feedback_id = request.POST.get('id')
        feedback_is = Teacher_Feedback.objects.get(id=feedback_id)
        feedback_is.feedback_reply = Reply
        feedback_is.save()

        return redirect('hod_feedback')


@login_required(login_url='login') 
def hod_feedback_guest_reply(request):
    if request.method == "POST":
        Reply = request.POST.get('Reply')
        feedback_id = request.POST.get('id')
        feedback_is = Guest_Feedback.objects.get(id=feedback_id)
        feedback_is.feedback_reply = Reply
        feedback_is.save()

        return redirect('hod_feedback')

        

# Events Section Strat        
@login_required(login_url='login')
def Event(request):
    event = Events.objects.all()
    data = {
        'events':event
    }
    return render (request,'HOD/HOD_events.html',data)

@login_required(login_url='login')
def Events_add(request):
    if request.method == "POST":
         events_dis = request.POST.get('events_discription')
         events_name = request.POST.get('events_name')
         events_date = request.POST.get('events_date')
          
         events = Events (
             Events_Name = events_name,
             Events_Discription = events_dis,
             Events_Date = events_date
         )
         events.save()
         return redirect('hod_events')
    return render (request,'HOD/HOD_events_add.html')

@login_required(login_url='login')    
def Events_update(request):
    if request.method == "POST":
        events_dis = request.POST.get('events_discription')
        events_name = request.POST.get('events_name')
        events_date = request.POST.get('events_date')

        Sid = request.POST.get('Sid')

        events = Events.objects.get(id = Sid)
        events.Events_Name = events_name
        events.Events_Date = events_date
        events.Events_Discription = events_dis
        events.save()

    return redirect('hod_events')

@login_required(login_url='login')
def Events_delete(request ,id):
    events = Events.objects.get(id = id)
    events.delete()
    
    return  redirect ('hod_events')

@login_required(login_url='login')
def Events_edit(request ,id):
    events = Events.objects.get(id = id)
    data = {
        'events':events
    }
    return render (request,'HOD/hod_events_edit.html',data)    

# End Events Section    

# start timetable section
@login_required(login_url='login')
def Time_Table(request):
    time = TimeTable.objects.all()
    data = {
        'timetable':time,
        'request': request
    }
    return render(request,'HOD/time_table.html',data)

@login_required(login_url='login')
def Time_Table_add(request):
    if request.method == "POST":
        section_name  = request.POST.get('section')
        sectionis = Section.objects.get(id=section_name)
        subject_name = request.POST.get('subject')
        subjectis = Subject.objects.get(id=subject_name)
        staffid = request.POST.get('staff_id')
        staffidis = int(staffid)
        staff = Teacher.objects.get(id=staffidis)
        day = request.POST.get('Day')
        
        starttime = request.POST.get('start_time')
        endtime = request.POST.get('end_time')
        if request.POST.get('OffTime') == '1':
            subjectis = None
        print(subjectis)
        time_table = TimeTable(
                Day = day,
                start_time = starttime,
                end_time = endtime, 
                section = sectionis,
                
                Subject = subjectis,
                staff_id = staff
            )
        time_table.save()
        
            
        return redirect('timetable')    
        
    subject = Subject.objects.all()
    section = Section.objects.all()
    data = {
        'subject':subject,
        'section':section
    }
    
    return render(request,'HOD/hod_add_time_table.html',data)

# end timetable section

# start Subject section
@login_required(login_url='login')
def subjects(request):
    subject = Subject.objects.all()
    data = {
        'subject':subject,
        'request': request
    }
    return render(request,'HOD/subject.html', data)

@login_required(login_url='login')
def add_subject(request):
    SECe = Section.objects.all()
    data = {
        'section':SECe
    }
    return render(request,'HOD/add_subject.html',data)

@login_required(login_url='login')
def subject_delete(request ,id):
    SECn = Subject.objects.get(id = id)
    SECn.delete()
    
    return  redirect ('sections')    

@login_required(login_url='login')    
def save_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject')
        subject_Secetion = request.POST.get('section')
        fm = request.POST.get('fm')
        pm = request.POST.get('pm')
       
        section = Section.objects.get(id=subject_Secetion)
        subject = Subject(
            Subject_Name = subject_name,
            Subject_Section = section,
            Full_Mark = fm,
            Pass_Mark = pm,
          

        )
        subject.save()
        messages.success(request,'Subject is Save !')
    return redirect('subjects')    
# end Subject Section

# start Section section 
@login_required(login_url='login')
def sections(request):
    SECe = Section.objects.all()
    data = {
        'section':SECe,
        'request': request
    }
    return render(request,'HOD/sections.html',data)

@login_required(login_url='login')    
def add_sections(request):
    classs = Class.objects.all()
    data = {
        'Class':classs
    }
    
    return render(request,'HOD/add_sections.html',data)


@login_required(login_url='login')    
def save_sections(request):
    if request.method == "POST":
        section_name = request.POST.get('section_name')
        section_Class = request.POST.get('Class_id')
        class_section = Class.objects.get(id=section_Class)
        section = Section(
            Section_Name = section_name,
            Class_Name = class_section
        )    
        section.save()
        messages.success(request,'Section is Save !')
    return redirect('sections')

@login_required(login_url='login')
def section_delete(request ,id):
    SECn = Section.objects.get(id = id)
    SECn.delete()
    
    return  redirect ('sections')
# @login_required(login_url='login')
# def section_update(request):
   
#     return  redirect ('sections')

# @login_required(login_url='login')
# def Section_edit(request ,id):
#     section = Section.objects.get(id = id)
#     Classs = Class.objects.all()
#     data = {
#         'section':section,
#         'Class':Classs
#     }
#     return render (request,'HOD/section_edit.html',data)    

# end Section section 

# start exam section
@login_required(login_url='login')
def ExamSave(request):
    exam = ExamEvent.objects.all()
    data = {
        'exams':exam
    }
    return render(request,'HOD/exam.html',data)


@login_required(login_url='login')
def ExamAdd(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject')
        subjectis = Subject.objects.get(id=subject_id)

        section_id = request.POST.get('section')
        sectionis = Section.objects.get(id=section_id)

        session_id = request.POST.get('session')
        sessionis = Exam.objects.get(id=session_id)

        staff_id = request.POST.get('staff_id')
        staff= int(staff_id)
        staffis = Teacher.objects.get(id=staff)



        start_time = request.POST.get('start_time')
        roomno = request.POST.get('roomno')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        Exams = ExamEvent(
            Date = date,
            StartTime = start_time,
            RoomNO =  roomno,
            subject = subjectis,
            section = sectionis,
            staff_id = staffis,
            end_time = end_time,
            Exam_Session = sessionis
        )
        Exams.save()
        return redirect('hod_exam')


    section = Section.objects.all()
    subject = Subject.objects.all()
    session = Exam.objects.all()
    data = {
        'section':section,
        'subject':subject,
        'session':session
    }
    return render(request,'HOD/add_exam.html',data)

@login_required(login_url='login')
def ExamDelete(request,id):
    exam = ExamEvent.objects.get(id = id )
    exam.delete()
    return redirect('hod_exam')    
# end exam section

# attendace vies
@login_required(login_url='login')
def AttendanceView(request):
   

       Attendance = AttendanceRecord.objects.all()
       
       data = {
        'student':Attendance,
        'request': request
       }

       return render(request,'HOD/view_attendance.html',data)

# end attendance view

def add_monthly_fees_for_all_students():
        # get the current date
        today = datetime.date.today()

        # get the month and year of the current date
        current_month = today.month
        current_year = today.year
        

        # retrieve all students from the database
        all_students = student.objects.all()

        # loop through all students
        for my_student in all_students:
            # get the class object associated with the student
            my_class = my_student.student_class

            # retrieve the monthly fee for the class
            monthly_fee = my_class.Monthly_Fee
        

            # check if the student has already paid for the current month
            if Fees.objects.filter(student=my_student, month=current_month,year=current_year,fee_type='Monthly Fee').exists():
                continue  # skip to the next student

            # create a new Fees object for the student
            new_fees = Fees(
                student=my_student,
            
                month = current_month,
                year = current_year,
                fee_type='Monthly Fee',
                amount=monthly_fee,
                
                transaction_id='Monthly Fees for ' + today.strftime("%B, %Y"),
                
            )

            # save the new Fees object to the database
            new_fees.save()
        # return  redirect('fees')    


def add_annual_fees_for_all_students():
        # get the current date
        today = datetime.date.today()

        # get the month and year of the current date
        current_month = today.month
        current_year = today.year
        

        # retrieve all students from the database
        all_students = student.objects.all()

        # loop through all students
        for my_student in all_students:
            # get the class object associated with the student
            my_class = my_student.student_class

            # retrieve the monthly fee for the class
            annual_fee = my_class.Annual_Fee
        

            # check if the student has already paid for the current month
            if Fees.objects.filter(student=my_student,year=current_year,fee_type='Annual Fee').exists():
                continue  # skip to the next student

            # create a new Fees object for the student
            new_fees = Fees(
                student=my_student,
            
                month = current_month,
                year = current_year,
                fee_type='Annual Fee',
                amount=annual_fee,
                
                transaction_id='Annual Fees for ' + today.strftime("%B, %Y"),
                
            )

            # save the new Fees object to the database
            new_fees.save()
        # return  redirect('fees')    

@login_required(login_url='login')
def add_exam_fees_for_all_students(request):
        # get the current date
        today = datetime.date.today()

        # get the month and year of the current date
        current_month = today.month
        current_year = today.year
        

        # retrieve all students from the database
        all_students = student.objects.all()

        # loop through all students
        for my_student in all_students:
            # get the class object associated with the student
            my_class = my_student.student_class

            # retrieve the monthly fee for the class
            Exams_Fee = my_class.Exams_Fee
        

            # check if the student has already paid for the current month
            if Fees.objects.filter(student=my_student, month=current_month,year=current_year,fee_type='Exam Fee').exists():
                continue  # skip to the next student

            # create a new Fees object for the student
            new_fees = Fees(
                student=my_student,
            
                month = current_month,
                year = current_year,
                fee_type='Exam Fee',
                amount=Exams_Fee,
                
                transaction_id='Exam Fees for ' + today.strftime("%B, %Y"),
                
            )

            # save the new Fees object to the database
            new_fees.save()
        return  redirect('fees')    


def add_hosteler_fees_for_all_rooms():
    # get the current date
    today = datetime.date.today()

    # get the month and year of the current date
    current_month = today.month
    current_year = today.year

    # retrieve all rooms from the database
    all_rooms = Room.objects.all()

    # loop through all rooms
    for my_room in all_rooms:
        # retrieve the room capacity and fee
        room_capacity = my_room.room_capacity
        room_fee = my_room.fees

        # retrieve the hostelers in the room
        all_hostelers = my_room.hostelers.all()

        # calculate the total fee for the room
        total_fee = room_capacity * room_fee

        # calculate the fee per hosteler
        if all_hostelers.count() > 0:
            fee_per_hosteler = total_fee / all_hostelers.count()
        else:
            fee_per_hosteler = 0

        # loop through all hostelers in the room
        for my_hosteler in all_hostelers:
            # check if the hosteler has already paid for the current month
            if Fees.objects.filter(student=my_hosteler.hosteler, month=current_month, year=current_year, fee_type='Hosteler Fee').exists():
                continue  # skip to the next hosteler

            # create a new Fees object for the hosteler
            new_fees = Fees(
                student=my_hosteler.hosteler,
                month=current_month,
                year=current_year,
                fee_type='Hosteler Fee',
                amount=fee_per_hosteler,
                transaction_id='Hosteler Fees for ' + today.strftime("%B, %Y"),
            )

            # save the new Fees object to the database
            new_fees.save()



def add_bus_riders_fees():
    # get the current date
    today = datetime.date.today()

    # get the month and year of the current date
    current_month = today.month
    current_year = today.year

    # retrieve all active bus riders from the database
    all_riders = bus_rider.active_riders.all()

    # loop through all bus riders
    for rider in all_riders:
        # check if the rider has already paid for the current month
        if Fees.objects.filter(student=rider.name, month=current_month, year=current_year, fee_type='Rider Fee').exists():
            continue  # skip to the next rider

        # create a new Fees object for the rider
        new_fees = Fees(
            student=rider.name,
            month=current_month,
            year=current_year,
            fee_type='Rider Fee',
            amount=rider.fees,
            transaction_id='Rider Fees for ' + today.strftime("%B, %Y"),
        )

        # save the new Fees object to the database
        new_fees.save()

@login_required(login_url='login')
def fees(request):

  
    unpaid_fees = Fees.objects.filter(payed=False).order_by('student')
    students = set(fee.student for fee in unpaid_fees)
    add_monthly_fees_for_all_students()
    add_annual_fees_for_all_students()
    add_hosteler_fees_for_all_rooms()
    add_bus_riders_fees()


    data = {'students': [],'request': request}
    for student in students:
        fees = unpaid_fees.filter(student=student)
        total_amount = fees.aggregate(total_amount=Sum('amount'))['total_amount']

        if fees.count() >= 1:
            data['students'].append({
                'id': student.id,
                'name': student.admin.username,
                'fees': [{'id': fee.id,  'amount': fee.amount ,  'transaction_id':fee.transaction_id} for fee in fees],
                'total_amount': total_amount
            })

    return render(request, 'HOD/fees.html', data)

@login_required(login_url='login')
def fees_history(request):
    paid_fees = Fees.objects.filter(payed=True).order_by('student')
    students = set(fee.student for fee in paid_fees)

    data = {'students': []}
    for student in students:
        fees = paid_fees.filter(student=student)
        # Get the number of monthly fees paid
        monthly_fees = fees.filter(fee_type='Monthly Fee').count()

            # Get the number of annual fees paid
        annual_fees = fees.filter(fee_type='Annual Fee').count()

            # Get the number of exam fees paid
        exam_fees = fees.filter(fee_type='Exam Fee').count()

            # Calculate the total fees paid
        total_fees = (monthly_fees * student.student_class.Monthly_Fee) + (annual_fees * student.student_class.Annual_Fee) + (exam_fees * student.student_class.Exams_Fee)

        if fees.count() >= 1:
            data['students'].append({
                'id': student.id,
                'name': student.admin.username,
                'fees': [{'id': fee.id,  'amount': fee.amount ,  'transaction_id':fee.transaction_id} for fee in fees],
                'total_amount': total_fees
            })

            
            

    return render(request, 'HOD/fees_history.html', data)

# add fees
@login_required(login_url='login')
def fees_Pay(request, id):
    fee = Fees.objects.get(id=id)
    fees = Fees.objects.filter(id=id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = Decimal(request.POST.get('amount'))
        if amount == fee.amount:
            fee.amount -= amount
            fee.payed = True
        else:
            fee.amount -= amount
        fee.payment_method = payment_method
        fee.save()
        return redirect('fees')  # or any other URL you want to redirect to

    data = {
        'fee': fee,
        'fees':fees
    }
    return render(request, 'HOD/pay_fees.html', data)

# end fees 

# Hostel start
@login_required(login_url='login')
def hostel_(request):
    hostels = Hostel.objects.annotate(
        num_rooms=Count('rooms'),
        num_occupied_rooms=Count('rooms', filter=Q(rooms__status='occupied')),
        num_available_rooms=Count('rooms', filter=Q(rooms__status='available'))
    )
    return render(request,'HOD/Hostel.html',{'hostels': hostels,'request': request})

@login_required(login_url='login')    
def hostel_add(request):
    staff = Staffs.objects.all()
    if request.method == 'POST':
        H_name = request.POST.get('hostel_name')
        warden = request.POST.get('warden')
        H_Number = request.POST.get('Number')
   
        H_email = request.POST.get('email')
        H_location = request.POST.get('location')
        H_address = request.POST.get('address')
        H_Photo = request.FILES.get('hostel_photo')
        H_warden = Staffs.objects.get(id = warden)
        facilities_ids = request.POST.getlist('facilities')
        H_Save = Hostel(
            name = H_name,
            warden = H_warden,
            location = H_location,
            address = H_address,
            phone_number = H_Number,
            email = H_email,
          
           
            hostel_photo = H_Photo
            
        )
        H_Save.save()
        # Set the related facilities for the hostel using the .set() method
        H_Save.facilities.set(facilities_ids)

        return redirect('hostel')
    data = {
        
        'staff':staff,
        'facilities': Facility.objects.all()
    }    
    return render(request,'HOD/Hostel_add.html',data)

# Hostel end 
# RoomAdd start
@login_required(login_url='login')
def hostel_R(request,id):
   try: 
    rooms = Room.objects.filter(hostel = id)
    room = Room.objects.get(hostel = id)
    hosteler_list = hostelers.objects.filter(room=room)
    hid = id
    data  = {
        'rooms':rooms,
        'hid':hid,
        'hosteler_list': hosteler_list,
        
    }
    return render(request,'HOD/RoomS.html',data)
   except:
    return render(request,'HOD/RoomS.html')
            
@login_required(login_url='login')
def RooMS_Add(request,id):
    hid = id
    data  = {
       
        'hid':hid
        
    }
    if request.method == 'POST':
        R_num = request.POST.get('room_num')
        R_Cap = request.POST.get('capacity')
        R_Type = request.POST.get('room_type')
        R_fee = request.POST.get('fee')
        R_Photo = request.FILES.get('r_photo')
        R_hostel = Hostel.objects.get(id = id)
        if Room.objects.filter(hostel = id, room_number = R_num , room_type = R_Type):
            return redirect('room_add',id)

        R_Save = Room(
            hostel = R_hostel,
            room_number = R_num,
            rooms_photo = R_Photo,
            room_capacity = R_Cap,
            room_type = R_Type,
            fees = R_fee,
            status = 'available'
        )    
        R_Save.save()
        return redirect('hostel_r',id)

    return render(request,'HOD/RoomS_Add.html',data)

@login_required(login_url='login')
def hostel_R_H(request, id):
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        room = Room.objects.get(hostel=id)
        studentis = student.objects.get(id=stu_id)

        if room.has_space():
            s = studentis
            hostelers_obj = hostelers(room=room, hosteler=s)
            hostelers_obj.save()

            if not room.has_space():
                room.status = 'occupied'
                room.save()

            return redirect('hostel_r', id)
        else:
            return redirect('hostel_r_h', id)

    return render(request, 'HOD/add_Hosteler.html')


# RoomAdd End

# transportiion section is start here

@login_required(login_url='login')
def Transport(request):
    tran = vehicles.objects.all()
    data = {
        'tra':tran,
        'request': request
    }
    return render(request,'HOD/transpotation.html',data)

@login_required(login_url='login')
def Transport_Route(request , id):
    route = Route.objects.filter(vehicle = id)
    hid = id 
    data = {
        'route':route,
        'hid':hid
    }
    return render(request,'HOD/route.html',data)

@login_required(login_url='login')
def Transport_Route_Ad(request , id):
    
    hid = id 
    
    
    if request.method == "POST":
        r_n = request.POST.get('route_name')
        s_l = request.POST.get('start_location')
        e_l = request.POST.get('end_location')
        vehiclesis = vehicles.objects.get(id = hid)
        R_save = Route(
            route_name = r_n,
            start_location = s_l,
            end_location = e_l,
            vehicle = vehiclesis
        )
        R_save.save()
        return redirect('transport_R1' , hid)
    return render(request,'HOD/route_add.html')

@login_required(login_url='login')
def Transport_V2(request):
    Staff_add = Staffs.objects.all()
    data = {
        'staff':Staff_add
    }
    
    if request.method == "POST":
        v_type = request.POST.get('vehiclesT')
        v_num = request.POST.get('vehiclesN')
        v_cap = request.POST.get('vehiclesC')
        v_driver = request.POST.get('driver')
        v_driveris = Staffs.objects.get(id = v_driver)
        v_Photo = request.FILES.get('v_photo')
        V_Save = vehicles(
            vehicle_type = v_type,
            vehicle_num = v_num,
            vehicles_capcity = v_cap,
            driver = v_driveris,
            vehicles_photo = v_Photo
        )
        V_Save.save()
        return redirect('transport')
    return render(request,'HOD/vehicles_add.html',data)




@login_required(login_url='login')
def Stops(request,id):
    hid = id 
    stop = Stop.objects.filter(vehicle = hid)
    data = {
        'stop':stop,
        'hid':hid
    }
    return render(request,'HOD/stops.html',data)

@login_required(login_url='login')
def Stops_add(request,id):
    hid = id 
    if request.method == "POST":
        s_n = request.POST.get('s_name')
        Latitude = request.POST.get('latitude')
        Longitude = request.POST.get('longitude')
        vehiclesis = vehicles.objects.get(id = hid)

        S_Save = Stop(
                stop_name = s_n,
                vehicle = vehiclesis,
                latitude = Latitude,
                longitude = Longitude
        )
        S_Save.save()
        return redirect('stops' , hid)
    
   
    return render(request,'HOD/stops_add.html')


@login_required(login_url='login')
def add_rider(request,id):
    hid = id
    vehicl = vehicles.objects.get(id =hid )
    if request.method == 'POST':
        name_id = request.POST.get('name')
        nameis = student.objects.get(id = name_id)
        
        fees = request.POST.get('fees')
        route_id = request.POST.get('route')
        stop_id = request.POST.get('stop')
        pickup_time = request.POST.get('pickup_time')
        dropoff_time = request.POST.get('dropoff_time')
        rider = bus_rider(name=nameis, fees=fees, route_id=route_id, stop_id=stop_id, pickup_time=pickup_time, dropoff_time=dropoff_time)
       
        rider.save()
        return redirect('stops',hid)
        
    return render(request, 'HOD/add_rider.html', {'students': student.objects.all(), 'routes': Route.objects.filter(vehicle = vehicl), 'stops': Stop.objects.filter(vehicle = vehicl)}) 
# end transportion heree
# staff section is starats
@login_required(login_url='login')
def STAff(request):
    staff = Staffs.objects.all()
    if staff:
      for i in staff:
        staff_id = i.staff.id
        salary = Employe.objects.get(employe = staff_id)
        data = {
            'staff':staff,
            'slary':salary,
            'request': request
        }
        return render (request,'HOD/Staff.html',data)
    else:
      return render(request,'HOD/Staff.html')
      
@login_required(login_url='login')
def Staff_add(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        type_s = request.POST.get('type')
        typeis = Staff_Types.objects.get(id = type_s)
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('Number')
        gender = request.POST.get('gender')
        
        Experience = request.POST.get('Experience')
        

        Sallery = request.POST.get('Sallery')
        CitizenCard = request.POST.get('CitizenCard')
        password = request.POST.get('password')
        username = request.POST.get('username')
        staff_photo = request.FILES.get('teacher_photo')

        address = request.POST.get('address')
        if CustomUser.objects.filter(username=username ).exists():
           messages.error(request,'')
           return redirect('hod_student_add')
        if CustomUser.objects.filter(email=email ).exists():
           messages.error(request,'')
           return redirect('hod_student_add')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                profile_pic = staff_photo,
                user_type = 2

            )    
            user.set_password(password)
            user.save()

            staff = Staffs(
                staff = user,
                Staff_type = typeis,
                staff_gender = gender,
               
                staff_mobile = phone,
               
                staff_Experience = Experience,
                CitizenCard_Number = CitizenCard,
               
                staff_address = address,
                staff_photo = staff_photo
            )
            staff.save()
            Employes = Employe(
                employe  = user,
                salary = Sallery
            )
            Employes.save()
            
            messages.success(request,'Staff is Add')
            return redirect('hod_staffs')
        
    staff_typ = Staff_Types.objects.all()
    data = {
        'tpe':staff_typ

    }    
    return render (request,'HOD/Staff_add.html',data)

@login_required(login_url='login')
def Staff_update(request):
    if request.method == "POST":
         first_name = request.POST.get('first_name')
         Sid = request.POST.get('id')
         last_name = request.POST.get('last_name')
         email = request.POST.get('email')
         gender = request.POST.get('gender')
         Experience = request.POST.get('Experience')
         typ = request.POST.get('type')
         typis = Staff_Types.objects.get(id = typ)
        
         
         Sallery= request.POST.get('Sallery')
         phone= request.POST.get('Number')
         username = request.POST.get('username')
         password= request.POST.get('password')
         CitizenCard = request.POST.get('CitizenCard')
         teacher_photo = request.FILES.get('teacher_photo')
         address = request.POST.get('address')
         
         user = CustomUser.objects.get(id = Sid)
         user.last_name = last_name
         user.first_name = first_name
         user.email = email
         user.username = username
         if password != None and password != '':
            user.set_password(password)

         
         user.save()
         staff = Staffs.objects.get(staff = Sid)
         staff.staff_gender = gender
         
        
         staff.staff_mobile = phone
         staff.Staff_type = typis
         staff.staff_Experience = Experience
         staff.CitizenCard_Number = CitizenCard
         staff.staff_address = address
         if teacher_photo != None and teacher_photo != '':
            staff.staff_photo = teacher_photo
         staff.save()   
         slary = Employe.objects.get(employe = user)
         slary.salary = Sallery
         slary.save()

       

         messages.success(request,'Student are update')
        

    return redirect('hod_staffs')


@login_required(login_url='login')
def STAff_edit(request, id):
    staff_instance = Staffs.objects.get(id=id)
    salary = Employe.objects.get(employe = staff_instance.staff.id)
    staff_dict = {
        'id': staff_instance.staff.id,
        'username': staff_instance.staff.username,
        'first_name': staff_instance.staff.first_name,
        'last_name': staff_instance.staff.last_name,
        'email': staff_instance.staff.email,
        'staff_type': staff_instance.Staff_type.id,
        'staff_gender': staff_instance.staff_gender,
        'staff_mobile': staff_instance.staff_mobile,
        'staff_experience': staff_instance.staff_Experience,
        'citizen_card_number': staff_instance.CitizenCard_Number,
        'staff_address': staff_instance.staff_address,
        'staff_photo': staff_instance.staff_photo,
        'created_at': staff_instance.created_at,
        'updated_at': staff_instance.updated_at,
    }
    staff_types = Staff_Types.objects.all()

    data = {
        'staff': staff_dict,
        'staff_types': staff_types,
        'salary':salary
    }

    return render(request, 'HOD/staff_edit.html', data)



@login_required(login_url='login')
def Staff_detail(request ,id):
    staff = Staffs.objects.filter(id = id)
    data = {
        'staff':staff
    }
    return render (request,'HOD/staff_detail.html',data)



@login_required(login_url='login')
def Staff_delete(request ,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    
    return  redirect ('hod_staffs')

# end staff section here 
# start salary section herer 

def add_monthly_salary_for_all_employees():
    # get the current date
    today = datetime.date.today()

    # get the month and year of the current date
    current_month = today.month
    current_year = today.year

    # retrieve all employees from the database
    all_employees = Employe.objects.all()

    # loop through all employees
    for employee in all_employees:
        # retrieve the monthly salary for the employee
        monthly_salary = employee.salary

        # check if the employee has already been paid for the current month
        if Salarys.objects.filter(employe=employee, month=current_month, year=current_year).exists():
            continue  # skip to the next employee

        # create a new Salarys object for the employee
        new_salary = Salarys(
            employe=employee,
            amount=monthly_salary,
            month=current_month,
            year=current_year,
            salary_type='Monthly Salary',
            payment_method='Cash', # change payment_method to your desired method
            transaction_id='Monthly Salary for ' + today.strftime("%B, %Y"),
            payed=False
        )

        # save the new Salarys object to the database
        try:
            new_salary.save()
        except :
            # skip to the next employee if a UNIQUE constraint error occurs
            continue

@login_required(login_url='login')
def salary(request):
    unpaid_salaries = Salarys.objects.filter(payed=False).order_by('employe__employe__username')
    add_monthly_salary_for_all_employees()
    employes = set(salary.employe for salary in unpaid_salaries)
    data = {'employe': [],'request': request}
    for emp in employes:
        salaries = unpaid_salaries.filter(employe=emp)
        total_amount = salaries.aggregate(total_amount=Sum('amount'))['total_amount']

        if salaries.count() >= 1:
            data['employe'].append({
                'id': emp.id,
                'employe': emp.employe,
                'salarys': [{'id': salary.id, 'amount': salary.amount, 'transaction_id': salary.transaction_id} for salary in salaries],
                'total_amount': total_amount
            })

    return render(request, 'HOD/salary.html', data)

@login_required(login_url='login')
def salaryP(request, id):
    salary = Salarys.objects.get(id=id)
    Salarry = Salarys.objects.filter(id=id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = Decimal(request.POST.get('amount'))
        if amount == salary.amount:
            salary.amount -= amount
            salary.payed = True
        else:
            salary.amount -= amount
        salary.payment_method = payment_method
        salary.save()
        return redirect('salary')  # or any other URL you want to redirect to

    data = {
        'salary':salary,
        'salarry': Salarry
    }
    return render(request, 'HOD/pay_salary.html', data)

@login_required(login_url='login')
def salary_history(request):
    paid_salaries = Salarys.objects.filter(payed=True).order_by('employe')
    employees = set(salary.employe for salary in paid_salaries)

    data = {'employees': []}
    for employee in employees:
        salaries = paid_salaries.filter(employe=employee)

        # Get the number of monthly salaries paid
        monthly_salaries = salaries.filter(salary_type='Monthly Salary').count()

        
        # Calculate the total salaries paid
        total_salaries = (monthly_salaries * employee.salary)

        if salaries.count() >= 1:
            data['employees'].append({
                'id': employee.id,
                'name': employee.employe.username,
                'salaries': [{'id': salary.id, 'amount': salary.amount, 'transaction_id': salary.transaction_id} for salary in salaries],
                'total_amount': total_salaries
            })

    return render(request, 'HOD/salary_history.html', data)

# end salary section end

# starrt resul seciton d
@login_required(login_url='login')
def Result_C(request):
    classsall = Class.objects.all()
    data = {
        'class':classsall,
        'request': request
    }
    return render(request,'HOD/result.html',data)

@login_required(login_url='login')   
def Result_C_Section(request,id):
    section = Section.objects.filter(Class_Name__Class_Name  = id) 
    data = {
        'section':section
    }
    return render(request,'HOD/section_show_r.html',data)

@login_required(login_url='login')   
def Result_EL(request,id,sid):
    # Rs = Result.objects.filter(student__student_Section__Section_Name = sid)
    Rs = Exam.objects.all()
    clsa = id
    ses = sid
    data = {
        'exam':Rs,
        'class':clsa,
        'ses':ses
    }
    return render(request,'HOD/Result_El.html',data)

@login_required(login_url='login')   
def Result_C_SectionPStudnet(request, id, sid, ied):
    section = Section.objects.get(Section_Name=sid, Class_Name__Class_Name=id)
    students = student.objects.filter(student_Section__Class_Name__Class_Name=id,student_Section__Section_Name = sid)
    subjects = Subject.objects.filter(Subject_Section=section)
    results = Result.objects.filter(exam_session=ied, student__in=students)

    subject_data = []

    for studentP in students:
        student_results = results.filter(student=studentP)
        subject_results = []

        for subject in subjects:
            subject_result = student_results.filter(subject=subject).first()

            if subject_result:
                subject_marks = subject_result.marks_obtained
                subject_full_mark = subject.Full_Mark

                subject_percentage = (subject_marks / subject_full_mark) * 100
                subject_grade = get_grade_from_percentage(subject_percentage)
                if subject_result.pass_fail_status == True:
                    status = "Passed"
                else :
                    status = "Failed"    

                subject_results.append({
                    'subject': subject,
                    'marks_obtained': subject_marks,
                    'percentage': subject_percentage,
                    'grade': subject_grade,
                    'status':status
                })

        subject_data.append({
            'student': studentP,
            'results': subject_results,
        })

    data = {
        'section': section,
        'subject_data': subject_data,
        'class_name': id,
        'section_name' : sid,
        'exid': ied,
    }

    return render(request, 'HOD/student_show_r.html', data)


def get_grade_from_percentage(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

@login_required(login_url='login')   
def ResultAdd(request, id, sid, ied):
    students = student.objects.filter(student_Section__Class_Name__Class_Name=id,student_Section__Section_Name=sid)
    subjects = Subject.objects.filter(Subject_Section__Class_Name__Class_Name=id,Subject_Section__Section_Name=sid)
    section = Section.objects.get(Section_Name=sid , Class_Name__Class_Name = id)
    examsession = Exam.objects.get(id=ied)

    if request.method == 'POST':
        for student_id in request.POST.getlist('student'):
            student_obj = student.objects.get(id=student_id)
            for subject_id, subject_name in zip(request.POST.getlist('subject_id'), request.POST.getlist('subject_name')):
                subject_obj = Subject.objects.get(id=subject_id)
                marks_obtained = request.POST.get(f'marks_{subject_id}')
                pass_mark = subject_obj.Pass_Mark
                mark = int(marks_obtained)
                
                # Check if the student passed or failed the subject
                if mark < pass_mark:
                    pass_fail_status = False  # Failed
                else:
                    pass_fail_status = True  # Passed
                    
                result = Result(
                    student=student_obj,
                    subject=subject_obj,
                    marks_obtained=marks_obtained,
                    pass_fail_status=pass_fail_status,
                    exam_session=examsession
                )
                result.save()
            return redirect('result')

    data = {
        'student': students,
        'subject': subjects
    }
    return render(request, 'HOD/result_add.html', data)


# end result section here



# blog section start here
@login_required(login_url='login')   
def Hod_Blogs(request):
    blog = Blog.objects.all()
    data = {
        'blogs':blog,
        'request': request
    }
    return render(request , 'HOD/blogs_views.html',data)

@login_required(login_url='login')   
def Hod_Blog_add(request):
    if request.method == 'POST':
        # create a new blog post object
        new_post = Blog()

        # populate the fields of the new post object with the data from the form submission
        new_post.title = request.POST['title']
        new_post.body = request.POST['body']
        new_post.author = request.user
        new_post.category = Category.objects.get(id=request.POST['category'])
        new_post.slug = slugify(new_post.title)

        # handle the tags field, which is a many-to-many field
        tag_ids = request.POST.getlist('tags')
        new_post.save()
        new_post.tags.add(*tag_ids)

        # handle the optional image and video fields
        if request.FILES.get('image'):
            image_file = request.FILES['image']

            # Resize and compress the image
            image_data = PILImage.open(image_file)
            image_data.thumbnail((800, 800))  # Set the desired maximum dimensions
            output_buffer = BytesIO()
            image_data.save(output_buffer, format='JPEG', optimize=True, quality=70)  # Adjust the quality as needed

            # Save the optimized image
            new_post.image.save(image_file.name, output_buffer)

        if request.FILES.get('video'):
            video_file = request.FILES['video']

            # Perform video compression using appropriate library and settings
            # For example, you can use FFmpeg or moviepy library to compress the video file

            # Save the optimized video
            new_post.video.save(video_file.name, video_file)

        # save the new blog post object
        new_post.save()

        # redirect to the detail view for the new blog post
        return redirect('blog_detail', slugs=new_post.slug)

    # if the request method is GET, render the blog post template with the categories and tags
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'HOD/add_blog.html', {'categories': categories, 'tags': tags})
    
@login_required(login_url='login')   
def Hod_Blog_categories_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('hod_blogs')
    return render(request,'HOD/add_categories.html')

@login_required(login_url='login')   
def Hod_Blog_tags_cloud_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        Tag.objects.create(name=name)
        return redirect('hod_blogs')
    return render(request,'HOD/add_tags.html')

@login_required(login_url='login')   
def Hod_Blog_delete(request,slug):
    blog = Blog.objects.get(slug = slug)
    blog.delete()
    return redirect('hod_blogs')
# end blog sectigon end 


# start gallery here 
@login_required(login_url='login')   
def add_image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image_file')
        blog_id = request.POST.get('blog_id')

        # Get the blog instance to associate the image with
        blog = Blog.objects.get(id=blog_id)

        # Create the new image instance and associate it with the blog instance
        image = Image(title=title, blog=blog)

        # Resize and compress the image
        image_data = PILImage.open(image_file)
        image_data.thumbnail((800, 800))  # Set the desired maximum dimensions
        output_buffer = BytesIO()
        image_data.save(output_buffer, format='JPEG', optimize=True, quality=70)  # Adjust the quality as needed
        image.media_file.save(image_file.name, output_buffer)

        return redirect('image_save')

    else:
        # Get all categories to display in the select field
        blog = Blog.objects.filter(author=request.user.id)

        context = {
            'categories': blog,
            'request': request
        }

        return render(request, 'HOD/add_image__in.html', context)
# end gallery here


# admistion starat 
@login_required(login_url='login')   
def request_views(request):
    today = date.today()
    admission_requests = ParentHelp.objects.filter( admission_deadline__gte=today)
    data = {
        'admission_requests': admission_requests,
        'request': request
    }
    return render(request, 'HOD/request_views.html', data)

@login_required(login_url='login')   
def request_views_student(request,student_name):
    admission = ParentHelp.objects.get(child_name =student_name)
    data ={
        'admission':admission
    }
    return render(request,'HOD/request_detail.html',data)

# end admistions /


# news add  in 
@login_required(login_url='login')   
def HOD_News(request):
    return render(request,'HOD/add_news.html')

@login_required(login_url='login')   
def HOD_News_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        slug = slugify(title)
        new_article = News(title=title, content=content, image=image, slug=slug)
        new_article.save()
        messages.success(request, 'Article added successfully!')
        return redirect('hod_news')  # replace 'news_list' with your URL name for the news list page
# end news out 
@login_required(login_url='login')   
def contact_views(request):
    contacts = Contact.objects.all()[::-1][:25]
    current_year = datetime.datetime.now().year
    context = {
        'contacts': contacts,
        'year': current_year,  # Replace with current year
        'request': request
    }
    return render(request,'HOD/views_contact_froms.html',context)
