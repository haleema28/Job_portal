from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/employer/', views.register_employer, name='register_employer'),
    path('register/job_seeker/', views.register_job_seeker, name='register_job_seeker'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('company/', views.company_profile_view, name='company_profile'),
    path('company/edit/', views.company_profile_edit, name='company_profile_edit'),
] 