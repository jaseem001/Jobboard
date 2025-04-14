"""
URL configuration for jobboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from core import views
from django.contrib.auth import views as auth_views
from core.views import EmployerLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('register/', views.register, name='register'),
    path('post-job/', views.post_job, name='post-job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply-ob'),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/register/', auth_views.LoginView.as_view(template_name='register.html'), name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('apply/', views.apply_now,name='applynow'),
    path('call-employer/', views.call_employer,name='call_employer'),
    path('save-for-later/', views.save_for_later,name='save_for_later'),
    path('accounts/employer/login/', EmployerLoginView.as_view(), name='employer_login'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('<int:pk>/', views.job_detail, name='job_detail'),

]
