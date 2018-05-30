from django.contrib import admin
from accounts.models import UserProfile
from accounts.models import Student, Course, Grade

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Grade)


# After each model is added then need to run python manage.py makemigrations and then migrate
