from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from Blogs.models import Blog , Tag , Image
from django.utils.text import slugify
from FrontEnd.models import  Category
from django.db.models import Sum
from django.db.models import Max , F
from collections import defaultdict
from datetime import datetime

#Pylint(E1101:no-member)

@login_required(login_url='login')
def Index(request):
    student_obj = student.objects.get(admin=request.user.id)
    attendance_records = AttendanceRecord.objects.filter(student_is=student_obj)
    student_ = request.user.student
    all_fees = Fees.objects.filter(student=student_)

    total_paid_fees, total_unpaid_fees = calculate_total_fees(all_fees)

    total_days, unique_student_parent_count = count_days_and_students(attendance_records)
    data = {
        'total_days': total_days,
        'parent_days': unique_student_parent_count,
        'paid_fees': total_paid_fees,
        'unpaid_fees': total_unpaid_fees
    }
    return render(request, 'Guest/guest_index.html', data)


def calculate_total_fees(queryset):
    total_unpaid_fees = queryset.filter(payed=False).aggregate(Sum('amount'))['amount__sum'] or 0
    paid_fees = queryset.filter(payed=True)
    total_paid_fees = sum((fee.student.student_class.Monthly_Fee if fee.fee_type == 'Monthly Fee' else fee.student.student_class.Annual_Fee if fee.fee_type == 'Annual Fee' else fee.student.student_class.Exams_Fee) * fee.amount for fee in paid_fees)
    return total_paid_fees, total_unpaid_fees

def count_days_and_students(queryset):
    total_days = queryset.count()

    student_parent_count = defaultdict(set)
    for record in queryset:
        student_id = record.student_is.student_id

        student_parent_count[student_id].add(record.date)

    unique_student_parent_count = len(student_parent_count)

    return total_days, unique_student_parent_count

@login_required(login_url='login')
def Guest_Notification_seen(request , status):
    notification = Guest_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('guest_Notification')

@login_required(login_url='login')
def Guest_notification(request):

    Studnet = student.objects.filter(admin = request.user.id)
    for i in Studnet:
       Student_id = i.id

       notification = Guest_Notification.objects.filter(guest_id = Student_id)[::-1][:4]
       
       data = {
        
        'notification':notification
       }

       return render(request , 'Guest/Guest_Notification.html' , data)
       

@login_required(login_url='login')
def Guest_Apply_leave(request):
    Studnet = student.objects.filter(admin = request.user.id)
    for i in Studnet:
       Student_id = i.id
       leave =  Student_leave.objects.filter(guest_id = Student_id)[::-1] [:10]
       data = {
            'leave':leave
        }

       return render(request,'Guest/aplly_leave.html',data)      

@login_required(login_url='login')
def Guest_Apply_leave_send(request):
    if request.method == "POST":
        leave_dateis = request.POST.get('leave_date')
        leave_subjectis = request.POST.get('leave_subject')
        leave_application = request.POST.get('application')

        guest = student.objects.get(admin = request.user.id)

        leave = Student_leave(
            guest_id = guest,
            leave_date = leave_dateis,
            leave_subject = leave_subjectis,
            Application = leave_application

        )
        leave.save()
        messages.success(request,'Leave is Send')


        return redirect('guest_apply_leave')       


@login_required(login_url='login')
def Guest__Feedback(request):
    guest = student.objects.get(admin = request.user.id)
    feedBack_history = Guest_Feedback.objects.filter(guest_id = guest)[::-1][:10]

    data = {
        'feedbackHistory':feedBack_history
    }

    return render(request , 'Guest/guest_feedback.html',data)


@login_required(login_url='login')
def Guest__Feedback_send(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        feedback_subjectis = request.POST.get('feedback_subject')
        guest = student.objects.get(admin = request.user.id)

        feedbackis = Guest_Feedback(
            feedback = feedback_message,
            feedback_subject = feedback_subjectis,
            guest_id = guest,
            feedback_reply = ''
        )
        feedbackis.save()
        messages.success(request,'Feedback Send')

    return redirect('guest_feedback')

@login_required(login_url='login')
def Guest_feedback_detail(request,status):
    detail = Guest_Feedback.objects.filter(id = status)
    data = {
        'detail':detail
    }
    return render(request,'Guest/feedback_deail.html',data)    

@login_required(login_url='login')
def Guest_Views_Attendance(request):
    Studnet = student.objects.filter(admin = request.user.id)
    for i in Studnet:
       Student_id = i.id

       Attendance = AttendanceRecord.objects.filter(student_is = Student_id)
       
       data = {
        'student':Attendance
       }



       return render(request,'Guest/views_attendance.html',data)


@login_required(login_url='login')
def Guest_Mettings(request):
    meetings = Meetings.objects.filter(Meetings_Type = '3')[::-1] [:10]
    data = {
        'meeting':meetings
    }
    return render(request, 'Guest/Metting.html',data)       

@login_required(login_url='login')
def Guest_Events(request):
    events = Events.objects.all()
    data = {
        'events':events,
    }
    return render(request,'Guest/Events.html',data)    

@login_required(login_url='login')
def Student_timetable(request):
    Student = student.objects.get(admin=request.user)
    timetable = TimeTable.objects.filter(section=Student.student_Section)
    context = {'tt': timetable}
    
    
    return render(request,'Guest/time_table.html',context)      

@login_required(login_url='login')
def exam_guest(request):
    Student = student.objects.get(admin=request.user)
    
    latest_exam = Exam.objects.filter(session_year__lte=datetime.now().year).annotate(max_session=Max('session_year')).filter(session_year=F('max_session')).order_by('-session_month').first()
    
    exams = ExamEvent.objects.filter(section=Student.student_Section, Exam_Session=latest_exam)
    
    context = {'ex': exams}
    
    return render(request, 'Guest/exams.html', context)


# blogs
@login_required(login_url='login')
def blog_add(request):

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
  
    return render(request,'Guest/add_blog.html', {'categories': categories, 'tags': tags})
    

@login_required(login_url='login')
def fees(request):
    Student = student.objects.get(admin=request.user)
    unpaid_fees = Fees.objects.filter(student=Student, payed=False).order_by('student')

    paid_fees = Fees.objects.filter(student=Student, payed=True).order_by('student')

    data = {'students': []}
    student_fees = paid_fees.filter(student=Student)
    # Get the number of monthly fees paid
    monthly_fees = student_fees.filter(fee_type='Monthly Fee').count()

    # Get the number of annual fees paid
    annual_fees = student_fees.filter(fee_type='Annual Fee').count()

    # Calculate the total fees paid
    total_fees = (monthly_fees * Student.student_class.Monthly_Fee) + (annual_fees * Student.student_class.Annual_Fee)

    if student_fees.count() >= 1:
        data['students'].append({
            'id': Student.id,
            'name': Student.admin.username,
            'fees': [{'id': fee.id, 'amount': fee.amount, 'transaction_id': fee.transaction_id} for fee in student_fees],
            'total_amount': total_fees
        })

    context = {
        'fees': unpaid_fees,
        'paid_fees': data['students']
    }
    return render(request, 'Guest/view_fees.html', context)

@login_required(login_url='login')
def view_result(request):
    student_ = request.user.student
    student_is = student.objects.get(admin=request.user.id)

    latest_exam = Exam.objects.filter(session_year__lte=datetime.now().year).annotate(max_session=Max('session_year')).filter(session_year=F('max_session')).order_by('-session_month').first()
    
    results = Result.objects.filter(student=student_, exam_session=latest_exam)
    total_full_mark = Subject.get_total_full_mark(student_.student_Section_id)
    
    context = {
        'results': results,
        'total_full_mark': total_full_mark,
        'studnet': student_is
    }
    return render(request, 'Guest/view_result.html', context)

@login_required(login_url='login')
def Image_blog_add(request):
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

