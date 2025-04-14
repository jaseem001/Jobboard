from django.urls import path, include
from django.contrib import admin 
from .import views
from .views import EmployerDashboardView


urlpatterns = [
    path('',views.home, name='home'),
    path('app/',views.home, name='home'),
    path('register/',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-job/',views.post_job, name='post-job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply-job'),
    path('dashboard', EmployerDashboardView.as_view(),name='employer_dashboard')
    
]


    

      
