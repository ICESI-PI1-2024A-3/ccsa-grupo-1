from django.contrib import admin
from .models import Subject, Class, Teacher, Program

# Register your models here.
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Program)
