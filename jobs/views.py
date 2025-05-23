from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Message
from accounts.models import User, CompanyProfile
from django import forms
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseForbidden
from django.core.mail import send_mail

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'duration', 'job_type', 'requirements', 'benefits']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']

# List all jobs
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    employer = request.GET.get('employer', '')
    if query:
        jobs = jobs.filter(title__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if employer:
        jobs = jobs.filter(employer__username__icontains=employer)
    context = {
        'jobs': jobs,
        'search_query': query,
        'search_location': location,
        'search_employer': employer,
    }
    return render(request, 'jobs/job_list.html', context)

# Job detail view
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Employer posts a job
@login_required
def job_post(request):
    if not request.user.role == 'employer':
        return redirect('job_list')
    # Check company profile completion
    try:
        profile = request.user.company_profile
        if not profile.company_name:
            messages.warning(request, 'Please complete your company profile before posting a job.')
            return redirect('company_profile_edit')
    except CompanyProfile.DoesNotExist:
        messages.warning(request, 'Please complete your company profile before posting a job.')
        return redirect('company_profile_edit')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_post.html', {'form': form})

# Job seeker applies to a job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if not request.user.role == 'job_seeker':
        return redirect('job_list')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = request.user
            application.save()
            messages.success(request, 'Applied successfully!')
            # Email notification to employer
            if job.employer.email:
                send_mail(
                    subject=f'New Application for {job.title}',
                    message=f'{request.user.username} has applied for your job: {job.title}.',
                    from_email=None,
                    recipient_list=[job.employer.email],
                )
            return redirect('job_seeker_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_dashboard(request):
    if not request.user.role == 'employer':
        return redirect('job_list')
    jobs = request.user.job_set.all().prefetch_related('applications')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

@login_required
def job_seeker_dashboard(request):
    if not request.user.role == 'job_seeker':
        return redirect('job_list')
    applications = request.user.application_set.select_related('job', 'job__employer').all()
    return render(request, 'jobs/job_seeker_dashboard.html', {'applications': applications})

@require_POST
@login_required
def update_application_status(request, app_id):
    if request.user.role != 'employer':
        return HttpResponseForbidden()
    from .models import Application
    app = Application.objects.select_related('job').get(pk=app_id)
    if app.job.employer != request.user:
        return HttpResponseForbidden()
    new_status = request.POST.get('status')
    if new_status in dict(Application.STATUS_CHOICES):
        app.status = new_status
        app.save()
        # Email notification to job seeker
        if app.job_seeker.email:
            send_mail(
                subject=f'Your Application for {app.job.title} - Status Update',
                message=f'Your application status for {app.job.title} is now: {app.get_status_display()}.',
                from_email=None,
                recipient_list=[app.job_seeker.email],
            )
    return redirect('employer_dashboard')

@login_required
def application_messages(request, app_id):
    app = Application.objects.select_related('job', 'job_seeker', 'job__employer').get(pk=app_id)
    if not (request.user == app.job.employer or request.user == app.job_seeker):
        return HttpResponseForbidden()
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(application=app, sender=request.user, content=content)
    messages_list = app.messages.select_related('sender').order_by('timestamp')
    return render(request, 'jobs/application_messages.html', {
        'application': app,
        'messages': messages_list,
    })
