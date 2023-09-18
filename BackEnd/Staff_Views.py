from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from tabulate import tabulate
from .models import *
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='login')
def STAFF_HOME(request):
    return render(request , 'Staff/Staff_index.html')

@login_required(login_url='login')
def STAFF_Notification_seen(request , status):
    notification = Staff_notifica.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')

@login_required(login_url='login')
def STAFF_Notification(request):

    staff = Staffs.objects.filter(staff = request.user.id)
    for i in staff:
       Staff_id = i.id

       notification = Staff_notifica.objects.filter(staff_id = Staff_id)[::-1][:4]
       
       data = {
        
        'notification':notification
       }

       return render(request , 'Staff/Staff_Notification.html' , data)

       
@login_required(login_url='login')
def STAFF_Apply_leave(request):
    staff = Staffs.objects.filter(staff = request.user.id)
    for i in staff:
        Staff_id = i.id
 
        leave =  Staff_leave.objects.filter(staff_id = Staff_id)[::-1][:4]
        data = {
            'leave':leave
        }
        return render(request,'Staff/aplly_leave.html',data)      

@login_required(login_url='login')
def STAFF_Apply_leave_send(request):
    if request.method == "POST":
        leave_dateis = request.POST.get('leave_date')
        leave_subjectis = request.POST.get('leave_subject')
        leave_application = request.POST.get('application')

        staff = Staffs.objects.get(staff = request.user.id)

        leave = Staff_leave(
            staff_id = staff,
            leave_date = leave_dateis,
            leave_subject = leave_subjectis,
            Application = leave_application

        )
        leave.save()
        messages.success(request,'Leave is Send')


        return redirect('staff_apply_leave')

@login_required(login_url='login')
def STAFF_feedback(request):
    staff = Staffs.objects.get(staff = request.user.id)
    feedBack_history = Staff_Feedback.objects.filter(staff_id = staff)[::-1][:4]

    data = {
        'feedbackHistory':feedBack_history
    }
    return render(request , 'Staff/Staff_feedback.html' ,data)

@login_required(login_url='login')
def STAFF_feedback_send(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        feedback_subjectis = request.POST.get('feedback_subject')
        staff = Staffs.objects.get(staff = request.user.id)

        feedbackis = Staff_Feedback(
            feedback = feedback_message,
            feedback_subject = feedback_subjectis,
            staff_id = staff,
            feedback_reply = ''
        )
        feedbackis.save()
        messages.success(request,'Feedback Send')

        return redirect('staff_feedback')

@login_required(login_url='login')        
def STAFF_feedback_detail(request,status):
    detail = Staff_Feedback.objects.filter(id = status)
    data = {
        'detail':detail
    }
    return render(request,'Staff/feedback_deail.html',data)

@login_required(login_url='login')
def Student_detail(request ,id):
    students = student.objects.filter(id = id)
    data = {
        'students':students
    }
    return render (request,'Staff/student_detail.html',data)

@login_required(login_url='login')
def STAFF_Mettings(request):
    meetings = Meetings.objects.filter(Meetings_Type = '1')[::-1][:10]
    data = {
        'meeting':meetings
    }
    return render(request, 'Staff/Metting.html',data)

@login_required(login_url='login')
def STAFF_Events(request):
    events = Events.objects.all()
    data = {
        'events':events,
    }
    return render(request,'Staff/Events.html',data)

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