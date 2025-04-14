from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Employer, JobSeeker, Job

admin.site.register(User, UserAdmin)
admin.site.register(Employer)
admin.site.register(JobSeeker)
admin.site.register(Job)