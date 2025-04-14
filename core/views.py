from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import (
    get_user_model, 
    authenticate, 
    login, 
    logout
    )
from django.contrib.auth.decorators import login_required
from .models import Job, JobSeeker, Employer, User
from .forms import (
    UserRegisterForm, 
    JobSeekerForm, 
    EmployerForm, 
    JobListingForm,
    UserCreationForm,
    CustomAuthenticationForm,
    EmployerLoginForm
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.core.exceptions import PermissionDenied
from .models import Job
from .forms import JobPostForm

# Home View
def home(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'home.html', {'jobs': jobs})

# Authentication Views
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Fixed: was passing request.user instead of request
            messages.success(request, 'Registration successful')
            return redirect('home')
        for error in errors:
            messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):

    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['pswd']
        red=authenticate(username=uname,password=password)
        print(red)
        if red is not None:
            login(request,red)
            f=red.first_name
            l=red.last_name
            return render(request,'home.html')
        else:

            
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')  # Fixed: Corrected typo in 'success'
    return redirect('home')

# Job Views
@login_required
def post_job(request):
    if not hasattr(request.user, 'employer'):
        raise PermissionDenied("Only employers can post jobs")
    
    if request.method == "POST":
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobListingForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    try:
        job = JobListing.objects.get(id=job_id, is_active=True)
    except JobListing.DoesNotExist:
        messages.error(request, 'Job not found')
        return redirect('home')

    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
    else:
        form = JobSeekerForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

# Simple Views
@login_required
def apply_now(request):
    return render(request, 'applynow.html')
@login_required
def call_employer(request):
    return render(request, 'callemployer.html')

@login_required
def save_for_later(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        # Add logic to save job for later
        messages.success(request, 'Job saved for later!')
    return render(request, 'saveforlater.html')

# Class-Based Views
class EmployerLoginView(LoginView):
    template_name = 'employer_login.html'
    authentication_form = EmployerLoginForm  # Use custom form for employer login
    
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_employer:
            messages.error(self.request, 'This account is not registered as an employer')
            return self.form_invalid(form)
        auth_login(self.request, user)
        messages.success(self.request, f'Welcome, {user.username}!')
        return redirect('employer_dashboard')

class EmployerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def test_func(self):
        return self.request.user.is_employer
    
    def handle_no_permission(self):
        messages.error(self.request, 'Access denied: Employer account required')
        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer = self.request.user.employer
        context['job_listings'] = JobListing.objects.filter(employer=employer)
        
        return context

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'job_list.html', {'jobs':jobs})
def job_detail(request, pk):
    job = get_object_or_404(Job,pk=pk)
    return render(request, 'job_detail.html', {'job':job})
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
        
    else:
        form = JobPostForm()
    return render(request, 'job_post.html',{'form':form})

@login_required
def my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs':jobs})