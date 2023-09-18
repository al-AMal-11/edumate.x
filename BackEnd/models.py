from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.gis.db.models import PointField
# Create your models here.
class CustomUser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2,'STAFFS'),
       
        (3,'GUEST'),
        (4,'TeacherT'),
        
    )
    user_type = models.CharField(choices=USER,max_length=58,default=1)
   
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True, null=True)
    bio = models.TextField()

class Class(models.Model):
    Class_Name = models.CharField(max_length=122)
    Monthly_Fee = models.IntegerField(default=2400)
    Annual_Fee = models.IntegerField(default=4000)
    Exams_Fee = models.IntegerField(default=400)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def get_number_of_sections(self):
        return self.section_set.count()

    def __str__(self) :
        return self.Class_Name


class Section(models.Model):
    Section_Name = models.CharField(max_length=122)
    Class_Name = models.ForeignKey(Class, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def get_number_of_students(self):
        return self.student_set.count()
    
    def __str__(self):
     return self.Class_Name.Class_Name + " - " + self.Section_Name    

class Subject(models.Model):
    Subject_Name = models.CharField(max_length=100)
    Full_Mark = models.IntegerField(default=100)
    Pass_Mark = models.IntegerField(default=75)
   
    Subject_Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Subject_Section.Class_Name.Class_Name + '-' + self.Subject_Name

    @classmethod
    def get_total_full_mark(self, section_id):
        subject_set = Subject.objects.filter(Subject_Section=section_id)
        total_full_mark = sum([s.Full_Mark for s in subject_set])
        return total_full_mark


class Staff_Types(models.Model):
    Type_Name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.Type_Name       

class Staffs(models.Model):
    Staff_type = models.OneToOneField(Staff_Types, on_delete=models.CASCADE)
    staff = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    staff_gender = models.CharField(max_length=100)
    staff_mobile = models.CharField(max_length=19)
    staff_Experience = models.CharField(max_length=100)
    CitizenCard_Number = models.CharField(max_length=30)
   
    staff_address = models.TextField()
    staff_photo = models.ImageField(upload_to='media/staff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.staff.username


class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    staff_gender = models.CharField(max_length=100)
    staff_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    class_Teacher = models.ForeignKey(Section , on_delete=models.CASCADE, null=True, blank=True)
    staff_mobile = models.CharField(max_length=19)
    staff_Qualification = models.CharField(max_length=100)
    staff_Experience = models.CharField(max_length=100)
    CitizenCard_Number = models.CharField(max_length=30)
   
    staff_address = models.TextField()
    staff_photo = models.ImageField(upload_to='media/Teacher_photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.admin.username + ' ' +self.admin.first_name
class Employe(models.Model):
    employe = models.OneToOneField(CustomUser,limit_choices_to={'user_type__in': [2, 4]} ,on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) :
        return  self.employe.username
class Salarys(models.Model):
    employe = models.OneToOneField(Employe,on_delete= models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(default=2)
    year = models.IntegerField(default=2023)
    payment_method = models.CharField(max_length=100)
    salary_type = models.CharField(max_length=100,default='Monthly Salary')
    transaction_id = models.CharField(max_length=100)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.employe.employe.username
    
class Meetings(models.Model):
    Meetings_Type = models.IntegerField(default=2)  
    Meeting_Name = models.CharField(max_length=100)
    Meeting_Date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return str(self.Meetings_Type) + '====' + self.Meeting_Name



class Staff_notifica(models.Model):

    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE) 
    Message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)
    def __str__(self) :
        return self.staff_id.staff.first_name + '' + self.staff_id.admin.last_name

class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=100 ,default='i')
    leave_subject = models.CharField(max_length=100,default='iam')
    Application = models.TextField()
    status = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.staff_id.staff.first_name + '-' + self.staff_id.admin.last_name




# studnt management is start here

class student(models.Model):

    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)    
    

    student_id = models.CharField(max_length=100)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    student_gender = models.CharField(max_length=100)
    student_dob = models.DateField()
    student_Religion = models.CharField(max_length=100)
    student_Joining_date = models.DateTimeField(auto_now_add=True)
    student_Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student_father_name = models.CharField(max_length=100)
    student_father_occupation = models.CharField(max_length=100)
    student_father_number = models.CharField(max_length=100)
    studen_present_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student_Feedback = models.TextField(default='Hi')
    studen_permanent_addres = models.TextField()
    Student_photo = models.ImageField(upload_to='media/Students_photos')
    def __str__(self) :
       return self.admin.first_name + "-" + self.admin.last_name    

    def get_total_marks(self):
        result_set = Result.objects.filter(student=self)
        total_marks = sum([r.marks_obtained for r in result_set])
        return total_marks   

    def get_percentage(self):
        total_marks = self.get_total_marks()
        total_full_mark = Subject.get_total_full_mark(self.student_Section)

        if total_full_mark > 0:
            percentage = (total_marks / total_full_mark) * 100
            return percentage
        else:
            return 0    

    def get_total_pass_mark(self):
        subject_set = Subject.objects.filter(Subject_Section=self.student_Section)
        total_pass_mark = sum([s.Pass_Mark for s in subject_set])
        return total_pass_mark

    def get_grade(self):
        percentage = self.get_percentage()
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

class Exam(models.Model):
    EXAM_TYPES = (
        ('firstterm', 'First Exam'),
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
    )
    name = models.CharField(max_length=100, default='EXAM - ')

    exam_type = models.CharField(max_length=255, choices=EXAM_TYPES)
    session_year = models.IntegerField()
    session_month = models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])

    def __str__(self):
        return f"{self.exam_type.capitalize()} - {self.session_year} - {self.get_session_month_display()}"

class Result(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    
    pass_fail_status = models.BooleanField()
   
    exam_session = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.admin.first_name}-{self.subject.Subject_Name}-{self.exam_session.name}"

    class Meta:
        unique_together = ('student', 'subject', 'exam_session')
        ordering = ['-exam_session__session_year', '-exam_session__session_month']


class Guest_Notification(models.Model):
    guest_id = models.ForeignKey(student,on_delete=models.CASCADE)
    Message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return 'Guest' + '-' + self.guest_id.student_father_name

class Student_leave(models.Model):
     guest_id = models.ForeignKey(student,on_delete=models.CASCADE)
     leave_date = models.CharField(max_length=100, default='iam')
     leave_subject = models.CharField(max_length=100,default='iamam')
     Application = models.TextField()
     status = models.IntegerField(default=0)
     create_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)

     def __str__(self) :
        return 'Student' + '-' + self.guest_id.admin.first_name + self.guest_id.admin.last_name


    
class Staff_Feedback(models.Model):
    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_subject = models.CharField(max_length=100,default='')
    feedback_reply = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.staff_id.staff.first_name + "-" + self.staff_id.admin.last_name


    
class Guest_Feedback(models.Model):
    guest_id = models.ForeignKey(student,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_subject = models.CharField(max_length=100,default='')
    feedback_reply = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.guest_id.admin.first_name + "-" + self.guest_id.admin.last_name

    
class AttendanceRecord(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student_is = models.ForeignKey(student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student_is.student_id + '-' + self.student_is.admin.first_name

class Events(models.Model):
    Events_Name = models.CharField(max_length=100)
    Events_Date = models.DateField()
    Events_Discription = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Events_Name + '-'+self.Events_Date

    




class TimeTable(models.Model):
    Day = models.CharField(max_length=100)
    staff_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    section = models.ForeignKey(Section,on_delete=models.CASCADE )
  
    start_time = models.TimeField()
    end_time = models.TimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.section.Section_Name


class ExamEvent(models.Model):
    Exam_Session = models.ForeignKey(Exam,on_delete=models.CASCADE)
    Date = models.DateField()
    StartTime = models.TimeField()
    RoomNO = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE )
    staff_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    end_time = models.TimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Date + '' + self.subject.Subject_Name + '-' + self.section.Section_Name
    
    
    


class Fees(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(default=2)
    year = models.IntegerField(default=2023)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student.admin.username
    
    def get_monthly_fee(self):
        return self.student.student_class.Monthly_Fee
    
    def get_annual_fee(self):
        return self.student.student_class.Annual_Fee
# Hostel start

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    warden = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    facilities = models.ManyToManyField('Facility')
    hostel_photo = models.ImageField(upload_to='media/Hostel_Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_all_room_ids():
        rooms = Room.objects.all()
        return [room.id for room in rooms]

    
    def __str__(self):
        return f"{self.name} - {self.location} @ {self.warden}"



class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    rooms_photo = models.ImageField(upload_to='media/Rooms_Image')
    room_capacity = models.IntegerField(default=1)
    room_type = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2,default = 1000)
    status = models.CharField(
        max_length=100, choices=[('available', 'Available'), ('occupied', 'Occupied')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def has_space(self):
        return self.hostelers.count() < self.room_capacity

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class Facility(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class hostelers(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='hostelers')
    hosteler = models.ForeignKey(student,on_delete=models.CASCADE)
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.room.has_space():
            raise ValueError('The room is full.')
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.room.hostel.name} - Room No . {self.room.room_number} - @ {self.hosteler.admin.username}"


# end Hostel code 

    
# transpotion section is strate




class vehicles(models.Model):
    vehicle_type = models.CharField(max_length=50)
    vehicle_num = models.CharField(max_length=50, unique=True)
    vehicles_capcity = models.IntegerField(default=1)
    driver = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    vehicles_photo = models.ImageField(upload_to='media/Vehicles_Img')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.vehicle_num


class Route(models.Model):
    route_name = models.CharField(max_length=50)
    start_location = models.CharField(max_length=50)
    end_location = models.CharField(max_length=50)
    vehicle = models.ForeignKey(vehicles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.route_name

class Stop(models.Model):
    stop_name = models.CharField(max_length=50)
    vehicle = models.ForeignKey(vehicles, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_riders(self):
        return self.bus_rider_set.all()

    def __str__(self):
        return self.stop_name

    

    
class ActiveRiderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class bus_rider(models.Model):
    name = models.ForeignKey(student, on_delete=models.CASCADE)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    route = models.ForeignKey(Route, on_delete=models.CASCADE ,  related_name='riders')
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_riders = ActiveRiderManager()

    def save(self, *args, **kwargs):
        riders_on_route = bus_rider.objects.filter(route=self.route, is_active=True)
        vehicle_capacity = self.route.vehicle.vehicles_capcity
        if len(riders_on_route) >= vehicle_capacity:
            raise ValidationError("Vehicle capacity reached")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name.admin.username


# end transpotion
# teacher section is StopAsyncIteratione
class Teacher_notification(models.Model):

    staff_id = models.ForeignKey(Teacher,on_delete=models.CASCADE) 
    Message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)
    def __str__(self) :
        return self.staff_id.admin.first_name + '' + self.staff_id.admin.last_name
class Teacher_Feedback(models.Model):
    staff_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_subject = models.CharField(max_length=100,default='')
    feedback_reply = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.staff_id.admin.first_name + "-" + self.staff_id.admin.last_name


class Teacher_leave(models.Model):
    staff_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=100 ,default='i')
    leave_subject = models.CharField(max_length=100,default='iam')
    Application = models.TextField()
    status = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.staff_id.admin.first_name + '-' + self.staff_id.admin.last_name

# end teacher