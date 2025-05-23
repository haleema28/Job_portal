from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, CompanyProfile
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied

# Create your views here.

class EmployerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'employer'
        if commit:
            user.save()
        return user

class JobSeekerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'job_seeker'
        if commit:
            user.save()
        return user

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'employer':
                return redirect('employer_dashboard')
            else:
                return redirect('job_seeker_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employer registered successfully!')
            return redirect('login')
    else:
        form = EmployerRegisterForm()
    return render(request, 'accounts/register_employer.html', {'form': form})

def register_job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Seeker registered successfully!')
            return redirect('login')
    else:
        form = JobSeekerRegisterForm()
    return render(request, 'accounts/register_job_seeker.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user_obj': request.user})

@login_required
def profile_edit(request):
    from django import forms
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'first_name', 'last_name']
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def company_profile_view(request):
    if request.user.role != 'employer':
        raise PermissionDenied
    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/company_profile.html', {'profile': profile})

@login_required
def company_profile_edit(request):
    if request.user.role != 'employer':
        raise PermissionDenied
    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    from django import forms
    class CompanyProfileForm(forms.ModelForm):
        class Meta:
            model = CompanyProfile
            fields = ['company_name', 'description', 'website', 'logo']
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated!')
            return redirect('company_profile')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'accounts/company_profile_edit.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            return redirect('employer_dashboard')
        elif request.user.role == 'job_seeker':
            return redirect('job_seeker_dashboard')
    return render(request, 'accounts/home.html')
