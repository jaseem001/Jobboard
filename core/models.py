from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    pass

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='employer_logos/', blank=True, null=True)
    
    def _str_(self):
        return self.company_name

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField()
    
    def _str_(self):
        return self.user.username

class Job(models.Model):
      
       employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
       title = models.CharField(max_length=200)
       company = models.CharField(max_length=200)
       location = models.CharField(max_length=200)
       description = models.TextField()
       requirements = models.TextField()
       salary = models.CharField(max_length=100, blank=True, null=True)
       job_type = models.CharField(max_length=50, choices=[
           ('full-time', 'Full Time'),
           ('part-time', 'Part Time'),
           ('freelance', 'Freelance'),
           ('remote','Remote')
       ])
       posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
       is_active = models.BooleanField(default=True)

       def _str_(self):
           return self.title