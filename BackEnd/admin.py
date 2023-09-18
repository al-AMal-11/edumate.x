from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','user_type']
admin.site.register(CustomUser , UserModel)
admin.site.register(student)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Meetings)
admin.site.register(Staff_notifica)
admin.site.register(Teacher_notification)
admin.site.register(Staff_leave)
admin.site.register(Teacher_leave)
admin.site.register(Guest_Notification)
admin.site.register(Student_leave)
admin.site.register(Staff_Feedback)
admin.site.register(Teacher_Feedback)
admin.site.register(Guest_Feedback)
admin.site.register(AttendanceRecord)
admin.site.register(Events)
admin.site.register(ExamEvent)
admin.site.register(TimeTable)
admin.site.register(Fees)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Facility)
admin.site.register(hostelers)
admin.site.register(Staff_Types)
admin.site.register(Staffs)
admin.site.register(Stop)
admin.site.register(vehicles)
admin.site.register(bus_rider)
admin.site.register(Route)
admin.site.register(Salarys)
admin.site.register(Employe)
admin.site.register(Result)
admin.site.register(Exam)

