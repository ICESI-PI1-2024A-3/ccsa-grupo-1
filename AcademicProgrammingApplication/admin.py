from django.contrib import admin
from .models import User, Role, Subject, Class, Teacher, Program

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Program)
