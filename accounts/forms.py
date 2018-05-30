from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Student, Course, Grade

SEMESTER = [
      ('Fall', 'Fall'),
      ('Spring', 'Spring'),
      ('Summer', 'Summer'),
]

YEAR = [
      ('2018', '2018'),
      ('2019', '2019'),
      ('2020', '2020'),
      ('2021', '2021'),
      ('2022', '2022'),
      ('2023', '2023'),
      ('2024', '2024'),  
      ('2025', '2025'),  
      ('2026', '2026'),  
      ('2027', '2027'),  
      ('2028', '2028'),  
      ('2029', '2029'),  
      ('2030', '2030'),  
]

GRADE = [
     ('A', 'A'), 
     ('B', 'B'), 
     ('C', 'C'), 
     ('D', 'D'), 
     ('F', 'F'), 
]

class RegistrationForm(UserCreationForm):
   email = forms.EmailField(required=True)
   first_name = forms.CharField(required=True)
   last_name = forms.CharField(required=True)

   class Meta: 
      model = User
      fields = (
         'username', 
         'first_name',
         'last_name',
         'email',
         'password1',
         'password2'
      )
   
   def saved(self, commit=True):
      user = super(RegistrationForm, self).save(commit=False)
      user.first_name = self.cleaned_data['first_name']
      user.last_name = self.cleaned_data['last_name']
      user.email = self.cleaned_data['email']

      if commit:
         user.save()

      return user

class StudentForm(forms.ModelForm):
    stud_firstname = forms.CharField(label=' Student First Name', max_length=50, required=True)
    stud_lastname = forms.CharField(label=' Student Last Name', max_length=50, required=True)
    stud_id = forms.IntegerField(label='Student ID')
    stud_maj = forms.CharField(label='Student\'s Major', max_length=50, required=True)

    class Meta:
        model = Student
        fields = (
            'stud_firstname',
            'stud_lastname',
            'stud_id',
            'stud_maj',
        )

class CourseForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name', max_length=50, required=True)
    course_id = forms.IntegerField(label='Course ID')
    course_teacher = forms.CharField(label='Course Teacher', max_length=30, required=True)
    course_semester = forms.CharField(label='Semester', widget=forms.Select(choices=SEMESTER))
    course_year = forms.CharField(label='Year', widget=forms.Select(choices=YEAR))

    class Meta:
        model = Course
        fields = (
            'course_name',
            'course_id',
            'course_teacher',
            'course_semester',
            'course_year',
        )

def get_courses():
      COURSES = []
      courses = Course.objects.all()
      for item in courses:
            COURSES.append((item.course_name, item.course_name),)
      
      return COURSES

def get_students():
      STUDENTS = []
      students= Student.objects.all()
      for item in students:
            STUDENTS.append((item.stud_id, item.stud_id),)
      
      return STUDENTS

class GradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.CharField(label='Student', widget=forms.Select(choices=get_students()))
        self.fields['course'] = forms.CharField(label='Course', widget=forms.Select(choices=get_courses()))
#     student = forms.CharField(label='Student', widget=forms.Select(choices=STUDENTS))
#     course = forms.CharField(label='Course', widget=forms.Select(choices=get_courses()))
    semester = forms.CharField(label='Semester', widget=forms.Select(choices=SEMESTER))
    year = forms.CharField(label='Year', widget=forms.Select(choices=YEAR))
    class_grade = forms.CharField(label='Class Grade', widget=forms.Select(choices=GRADE))
    lab_grade = forms.CharField(label='Lab Grade', widget=forms.Select(choices=GRADE))

    class Meta:
        model = Grade
        fields = (
            'student',
            'course',
            'semester',
            'year',
            'class_grade',
            'lab_grade',
        )