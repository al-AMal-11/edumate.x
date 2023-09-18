from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from tabulate import tabulate
from .models import *
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from Blogs.models import Blog , Tag , Image
from FrontEnd.models import  Category
from django.db.models import Max , F
from django.utils.text import slugify

@login_required(login_url='login')
def T_HOME(request):
    return render(request , 'Teacher/teacher_index.html')

@login_required(login_url='login')
def T_Notification_seen(request , status):
    notification = Teacher_notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('teacher_notification')

@login_required(login_url='login')
def T_Notification(request):

    staff = Teacher.objects.filter(admin = request.user.id)
    for i in staff:
       Staff_id = i.id

       notification = Teacher_notification.objects.filter(staff_id = Staff_id)[::-1][:4]
       
       data = {
        
        'notification':notification
       }

       return render(request , 'Teacher/Teacher_Notification.html' , data)

       
@login_required(login_url='login')
def T_Apply_leave(request):
    staff = Teacher.objects.filter(admin = request.user.id)
    for i in staff:
        Staff_id = i.id
 
        leave =  Teacher_leave.objects.filter(staff_id = Staff_id)[::-1][:4]
        data = {
            'leave':leave
        }
        return render(request,'Teacher/aplly_leave.html',data)      

@login_required(login_url='login')
def T_Apply_leave_send(request):
    if request.method == "POST":
        leave_dateis = request.POST.get('leave_date')
        leave_subjectis = request.POST.get('leave_subject')
        leave_application = request.POST.get('application')

        staff = Teacher.objects.get(admin = request.user.id)

        leave = Teacher_leave(
            staff_id = staff,
            leave_date = leave_dateis,
            leave_subject = leave_subjectis,
            Application = leave_application

        )
        leave.save()
        messages.success(request,'Leave is Send')


        return redirect('teacher_apply_leave')

@login_required(login_url='login')
def T_feedback(request):
    staff = Teacher.objects.get(admin = request.user.id)
    feedBack_history = Teacher_Feedback.objects.filter(staff_id = staff)[::-1][:4]

    data = {
        'feedbackHistory':feedBack_history
    }
    return render(request , 'Teacher/teacher_feedback.html' ,data)

@login_required(login_url='login')
def T_feedback_send(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        feedback_subjectis = request.POST.get('feedback_subject')
        staff = Teacher.objects.get(admin = request.user.id)

        feedbackis = Teacher_Feedback(
            feedback = feedback_message,
            feedback_subject = feedback_subjectis,
            staff_id = staff,
            feedback_reply = ''
        )
        feedbackis.save()
        messages.success(request,'Feedback Send')

        return redirect('teacher_feedback')

@login_required(login_url='login')        
def T_feedback_detail(request,status):
    detail = Teacher_Feedback.objects.filter(id = status)
    data = {
        'detail':detail
    }
    return render(request,'Teacher/feedback_deail.html',data)

@login_required(login_url='login')
def take_attandance(request):

        date = datetime.now().date()
        class_teacher_id = request.user.id
        staff = Teacher.objects.get(admin = class_teacher_id)
        ssection_id =staff.class_Teacher.id
        section = Section.objects.get(id=ssection_id)
        section_ = section

        
        students = student.objects.filter(student_Section=section_)
        # Assuming you have a Section instance called 'section'
        

        data = {
        'students': students,
            'date':date,

            'sectionis':section_
        }
        return render(request, 'Teacher/take_attandance.html',data)

def mark_absent(date, absent_list):
    attendance_records = AttendanceRecord.objects.filter(date=date, student_is__in=absent_list)
    for record in attendance_records:
        record.present = 0
        record.save()

@login_required(login_url='login')        
def take_attendance_send(request):

 if request.method == "POST":
    date = datetime.now().date()
    student_id_list = request.POST.getlist('student_id')
    class_teacher_id = request.user.id
    staff = Teacher.objects.get(admin = class_teacher_id)
    ssection_id =staff.class_Teacher.id
    section = Section.objects.get(id=ssection_id)
    section_ = section
    absent_list = request.POST.getlist('Value')

    for i in range(len(student_id_list)):
            student_id = student_id_list[i]
            
            Student = student.objects.get(id=student_id)
            present = 1

            attendance_record = AttendanceRecord(student_is=Student, section=section_, date=date, present=present)
            attendance_record.save()
    mark_absent(date, absent_list)    


    messages.success(request, "Attendance recorded successfully.")

    return redirect('teacher_take_attandance')
    
@login_required(login_url='login')
def Student_detail(request ,id):
    students = student.objects.filter(id = id)
    data = {
        'students':students
    }
    return render (request,'Teacher/student_detail.html',data)

@login_required(login_url='login')
def T_Mettings(request):
    meetings = Meetings.objects.all()[::-1][:10]
    data = {
        'meeting':meetings
    }
    return render(request, 'Teacher/Metting.html',data)

@login_required(login_url='login')
def T_timetable(request):
    staff = Teacher.objects.filter(admin = request.user.id)
    for i in staff:
        Staff_id = i.id
 
        timetable =  TimeTable.objects.filter(staff_id = Staff_id)
        data = {
            'timetable':timetable
        }
        return render(request,'Teacher/time_table.html',data)    
    

@login_required(login_url='login')
def exam_t(request):
    staff = Teacher.objects.filter(admin = request.user.id)
    for i in staff:
        Staff_id = i.id
 


        latest_exam = Exam.objects.filter(session_year__lte=datetime.now().year).annotate(max_session=Max('session_year')).filter(session_year=F('max_session')).order_by('-session_month').first()
    
        exams = ExamEvent.objects.filter(staff_id = Staff_id, Exam_Session=latest_exam)
    
        context = {'sta': exams}
        
        
        return render(request,'Teacher/exams.html',context)        
@login_required(login_url='login')
def T_add_blog(request):

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
            new_post.image = request.FILES['image']
        if request.FILES.get('video'):
            new_post.video = request.FILES['video']

        # save the new blog post object
        new_post.save()

        # redirect to the detail view for the new blog post
        return redirect('blog_detail', slugs=new_post.slug)

    # if the request method is GET, render the blog post template with the categories and tags
    categories = Category.objects.all()
    tags = Tag.objects.all()
  
    return render(request,'Teacher/add_blog.html', {'categories': categories, 'tags': tags})


@login_required(login_url='login')
def T_add_Image_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image_file')
        blog_id = request.POST.get('blog_id')

        # Get the blog instance to associate the image with
        blog = Blog.objects.get(id=blog_id)

        # Create the new image instance and associate it with the blog instance
        image = Image(title=title, media_file=image_file, blog=blog)
        image.save()

        return redirect('t_blogimage_add')

    else:
        # Get all categories to display in the select field
        blog = Blog.objects.filter(author = request.user.id)

        context = {
            'categories': blog
        }

        return render(request, 'HOD/add_image__in.html', context)
@login_required
def view_salary(request):
    # Retrieve the Salarys object associated with the currently logged-in employee
    salary = Salarys.objects.get(employe__employe=request.user)

    # Convert the salary data into a list of lists for tabulate
    salary_ = Employe.objects.get(employe = request.user)
    payed_salary = salary_.salary
    if salary.payed :
     salary_data = [

        [payed_salary, salary.month, salary.year, salary.payment_method,salary.salary_type, salary.transaction_id ,'Paid' if salary.payed else 'Not Paid'],
    
        
    ]
    else:
     salary_data = [

        [salary.amount , salary.month, salary.year, salary.payment_method,salary.salary_type, salary.transaction_id ,'Paid' if salary.payed else 'Not Paid'],
    
        
    ]

    # Generate the table using tabulate
    table = tabulate(salary_data, headers=['Amount', 'Month','Year','Payment Method' ,'Salary Type','Transaction ID','Status'], tablefmt='html')

    # Pass the table HTML to the template
    context = {'table': table,'salary':salary}
    return render(request, 'BACKEND/view_salary.html', context)
