from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('post/', views.job_post, name='job_post'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('job_seeker/dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('application/<int:app_id>/update_status/', views.update_application_status, name='update_application_status'),
    path('application/<int:app_id>/messages/', views.application_messages, name='application_messages'),
] 