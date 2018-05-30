from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import IntegerField

SEMESTER = []
YEAR = []
GRADE = []
COURSES = []
STUDENTS = []


# Create your models here.
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   description = models.CharField(max_length=100 , default='')
   phone = models.IntegerField(default=0)

   # custom manager replaces object manager
   objects = models.Manager()

def create_profile(sender, **kwargs):
   if kwargs['created']:
      user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Student(models.Model):
    stud_firstname = models.CharField(max_length=50)
    stud_lastname = models.CharField(max_length=50, null=True)
    stud_id = models.IntegerField()
    stud_maj = models.CharField(max_length=50, default='Chemistry')
    #user = models.ForeignKey(User)

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_id = models.IntegerField()
    course_teacher = models.CharField(max_length=30, default='Dr. Le')
    course_semester = models.CharField(max_length=6, choices=SEMESTER, default='fall')
    course_year = models.CharField(max_length=4, choices=YEAR, default='2018')

class Grade(models.Model):
    student = models.CharField(max_length=10, choices=STUDENTS, default='')
    course = models.CharField(max_length=50, choices=COURSES, default='')
    semester = models.CharField(max_length=6, choices=SEMESTER, default='')
    year = models.CharField(max_length=4, choices=YEAR, default='')
    class_grade = models.CharField(max_length=1, choices=GRADE, default='')
    lab_grade = models.CharField(max_length=1, choices=GRADE, default='')


# def create_student(sender, **kwargs):
#    if kwargs['created']:
#       students = Student.objects.create(user=kwargs['instance'])