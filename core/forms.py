from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import JobSeeker, Employer, Job

# Get the custom User model
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.replace('_', ' ').capitalize()
            })

class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    company_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name', 'company_description']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
            Employer.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_description=self.cleaned_data['company_description']
            )
        return user

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume', 'skills']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'website', 'logo']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }

class JobListingForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'job_type', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.capitalize()
            })

class EmployerLoginForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.capitalize()
            })  

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_employer:
            raise forms.ValidationError(
                "This account doesn't have employer privileges. Please login as a regular user or register as an employer.",
                code='invalid_login'
)
        
class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','company','location','description',
                  'requirements','job_type','salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows':5}),
            'requirements': forms.Textarea(attrs={'rows':5}),
        }