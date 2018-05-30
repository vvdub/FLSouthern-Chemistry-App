import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import StudentForm, CourseForm, GradeForm
from accounts.models import Course, Student, Grade
from django.views.generic import TemplateView, ListView
from django.db.models import Count, Q


# Create your views here.
@login_required
def home(request):
   args = {'user': request.user}
   return render(request, 'accounts/home.html', args)

def register(request):
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('/')
   else:
      form = RegistrationForm()
      
   args = {'form': form}
   return render(request, 'accounts/registration.html', args)

@login_required
def profile(request):
   args = {'user': request.user}
   return render(request, 'accounts/profile.html', args)

@login_required
def student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            first = form.cleaned_data['stud_firstname']
            last = form.cleaned_data['stud_lastname']
            id = form.cleaned_data['stud_id']
            major = form.cleaned_data['stud_maj']
            form = StudentForm()
            return redirect('/account')

            args = {'form': form, 'stud_firstname': stud_firstname, 'stud_lastname': stud_lastname,
                        'stud_id': stud_id, 'stud_maj': stud_maj}
            return render(request, 'accounts/student.html', args)
    else:
        form = StudentForm()
        return render(request, 'accounts/student.html', {'form': form})

@login_required
def course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['course_name']
            id = form.cleaned_data['course_id']
            teacher = form.cleaned_data['course_teacher']
            semester = form.cleaned_data['course_semester']
            year = form.cleaned_data['course_year']
            form = CourseForm()
            return redirect('/account')

            args = {'form': form, 'course_name': course_name, 'course_id': course_id, 'course_teacher':         course_teacher,'course_semester': course_semester, 'course_year': course_year}
            return render(request, 'accounts/course.html', args)
    else:
        form = CourseForm()
        return render(request, 'accounts/course.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'accounts/test.html', {'courses': courses})

@login_required
def grade(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year']
            class_grade = form.cleaned_data['class_grade']
            lab_grade = form.cleaned_data['lab_grade']
            form = GradeForm()
            return redirect('/account')

            args = {'form': form, 'student': student, 'course': course, 'semester': semester, 'year': year, 'class_grade': class_grade, 'lab_grade': lab_grade, 'courses': courses, 'students': students}
            return render(request, 'accounts/grade.html', args)
    else:
        form = GradeForm()
        return render(request, 'accounts/grade.html', {'form': form, 'courses': courses, 'students': students})

def info(request, id):
    course = Course.objects.get(id=id)
    student = Grade.objects.filter(course=course.course_name)
    datac = Grade.objects.filter(course=course.course_name) \
            .values('class_grade') \
            .annotate(class_a=Count('class_grade', filter=Q(class_grade='A')), class_b=Count('class_grade', filter=Q(class_grade='B')),
                        class_c=Count('class_grade', filter=Q(class_grade='C')), class_d=Count('class_grade', filter=Q(class_grade='D')),
                        class_f=Count('class_grade', filter=Q(class_grade='F'))) \
            .order_by('class_grade')

    class_a_data = list()
    g1 = 0
    class_b_data = list()
    g2 = 0
    class_c_data = list()
    g3 = 0
    class_d_data = list()
    g4 = 0
    class_f_data = list()
    g5 = 0

    for entry in datac:
        class_a_data.append(entry['class_a'])
        class_b_data.append(entry['class_b'])
        class_c_data.append(entry['class_c'])
        class_d_data.append(entry['class_d'])
        class_f_data.append(entry['class_f'])
    for x in class_a_data:
        g1 += x
    for x in class_b_data:
        g2 += x
    for x in class_c_data:
        g3 += x
    for x in class_d_data:
        g4 += x
    for x in class_f_data:
        g5 += x

    class_A = { 'name': 'A', 'y': g1}
    class_B = { 'name': 'B', 'y': g2}
    class_C = { 'name': 'C', 'y': g3}
    class_D = { 'name': 'D', 'y': g4}
    class_F = { 'name': 'F', 'y': g5}

    c_count = 0;

    if g1 != 0:
        c_count += 1
    if g2 != 0:
        c_count += 1
    if g3 != 0:
        c_count += 1
    if g4 != 0:
        c_count += 1
    if g5 != 0:
        c_count += 1

    if c_count != 0:
        cGrades = [class_A, class_B, class_C, class_D, class_F]
    else:
        cGrades = []

    class_chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Class Grades'},
		'plotOptions': {'pie': {'dataLabels': {'enabled': 'true', 'format': '<b>{point.name}</b>: {y}'}}},
        'series': [{'name': 'Grades', 'data': cGrades }]
    }

    class_dump = json.dumps(class_chart)

    datal = Grade.objects.filter(course=course.course_name) \
            .values('lab_grade') \
            .annotate(lab_a=Count('lab_grade', filter=Q(lab_grade='A')), lab_b=Count('lab_grade', filter=Q(lab_grade='B')),
                lab_c=Count('lab_grade', filter=Q(lab_grade='C')), lab_d=Count('lab_grade', filter=Q(lab_grade='D')),
                lab_f=Count('lab_grade', filter=Q(lab_grade='F'))) \
            .order_by('lab_grade')

    lab_a_data = list()
    L1 = 0
    lab_b_data = list()
    L2 = 0
    lab_c_data = list()
    L3 = 0
    lab_d_data = list()
    L4 = 0
    lab_f_data = list()
    L5 = 0

    for entry in datal:
        lab_a_data.append(entry['lab_a'])
        lab_b_data.append(entry['lab_b'])
        lab_c_data.append(entry['lab_c'])
        lab_d_data.append(entry['lab_d'])
        lab_f_data.append(entry['lab_f'])
    for x in lab_a_data:
        L1 += x
    for x in lab_b_data:
        L2 += x
    for x in lab_c_data:
        L3 += x
    for x in lab_d_data:
        L4 += x
    for x in lab_f_data:
        L5 += x

    labA = { 'name': 'A', 'y': L1}
    labB = { 'name': 'B', 'y': L2}
    labC = { 'name': 'C', 'y': L3}
    labD = { 'name': 'D', 'y': L4}
    labF = { 'name': 'F', 'y': L5}

    l_count = 0;

    if L1 != 0:
        l_count += 1
    if L2 != 0:
        l_count += 1
    if L3 != 0:
        l_count += 1
    if L4 != 0:
        l_count += 1
    if L5 != 0:
        l_count += 1

    if c_count != 0:
        lGrades = [labA, labB, labC, labD, labF]
    else:
        lGrades = []

    labChart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Lab Grades'},
        'plotOptions': {'pie': {'dataLabels': {'enabled': 'true', 'format': '<b>{point.name}</b>: {y}'}}},
        'series': [{'name': 'Grades', 'data': lGrades}]
    }

    lab_dump = json.dumps(labChart)
    args = {
     'course': course,
     'student': student,
     'Class': class_dump,
     'Lab': lab_dump
      }

    return render(request, 'accounts/info.html', args)

@login_required
def student_list(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    grades = Grade.objects.all()

    args = {'students': students, 'courses': courses, 'grades': grades}
    return render(request, 'accounts/all-students.html', args)

@login_required
def student_info(request, id):
    student = Student.objects.get(id=id)
    grades = Grade.objects.filter(student=student.stud_id)

    args = {'student': student, 'grades': grades}
    return render(request, 'accounts/student-info.html', args)

      
