from django.core.management.base import BaseCommand
from accounts.models import User, CompanyProfile
from jobs.models import Job, Application
from django.utils import timezone
import random
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Seed the database with dummy employers, job seekers, company profiles, jobs, and applications.'

    def handle(self, *args, **kwargs):
        # Create employers
        employers = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'employer{i+1}',
                defaults={
                    'email': f'employer{i+1}@company.com',
                    'role': 'employer',
                }
            )
            user.set_password('password123')
            user.save()
            profile, _ = CompanyProfile.objects.get_or_create(
                user=user,
                defaults={
                    'company_name': f'Company {i+1}',
                    'description': f'This is Company {i+1}, a great place to work.',
                    'website': f'https://company{i+1}.com',
                }
            )
            employers.append(user)
        self.stdout.write(self.style.SUCCESS('Created employers and company profiles.'))

        # Create job seekers
        job_seekers = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'seeker{i+1}',
                defaults={
                    'email': f'seeker{i+1}@mail.com',
                    'role': 'job_seeker',
                }
            )
            user.set_password('password123')
            user.save()
            job_seekers.append(user)
        self.stdout.write(self.style.SUCCESS('Created job seekers.'))

        # Create jobs
        jobs = []
        salary_options = [
            '$50,000 - $60,000 per year',
            '$70,000 - $90,000 per year',
            '$100,000 - $120,000 per year',
            '$30/hr',
            'Competitive',
        ]
        duration_options = [
            'Permanent',
            '6 months',
            '12 months',
            'Contract',
            'Part-time',
        ]
        job_type_options = [
            'Full-time',
            'Part-time',
            'Contract',
            'Remote',
        ]
        requirements_options = [
            'Bachelor degree in relevant field\n2+ years experience\nTeam player',
            'Strong communication skills\nPython, Django\nProblem-solving attitude',
            'Experience with React or Angular\nPortfolio of past projects',
            'Attention to detail\nAbility to work independently',
            'Knowledge of cloud platforms (AWS, Azure)',
        ]
        benefits_options = [
            'Health insurance\nRemote work\nFlexible hours',
            '401k matching\nPaid time off',
            'Free snacks\nGym membership',
            'Learning budget\nConference tickets',
            'Stock options\nAnnual bonus',
        ]
        for i in range(6):
            employer = random.choice(employers)
            job = Job.objects.create(
                employer=employer,
                title=f'Dummy Job {i+1}',
                description=f'This is a description for Dummy Job {i+1}.',
                location=random.choice(['New York', 'San Francisco', 'Remote', 'London', 'Berlin']),
                salary=random.choice(salary_options),
                duration=random.choice(duration_options),
                job_type=random.choice(job_type_options),
                requirements=random.choice(requirements_options),
                benefits=random.choice(benefits_options),
                posted_at=timezone.now() - timezone.timedelta(days=random.randint(0, 30)),
            )
            jobs.append(job)
        self.stdout.write(self.style.SUCCESS('Created jobs.'))

        # Create applications
        for seeker in job_seekers:
            applied_jobs = random.sample(jobs, k=random.randint(1, 3))
            for job in applied_jobs:
                resume_file = ContentFile(b"Dummy resume content.", name=f"resume_{seeker.username}_{job.id}.txt")
                app, created = Application.objects.get_or_create(
                    job=job,
                    job_seeker=seeker,
                    defaults={
                        'applied_at': timezone.now() - timezone.timedelta(days=random.randint(0, 10)),
                        'status': random.choice(['pending', 'reviewed', 'accepted', 'rejected'])
                    }
                )
                if created:
                    app.resume.save(resume_file.name, resume_file)
        self.stdout.write(self.style.SUCCESS('Created applications.'))

        self.stdout.write(self.style.SUCCESS('Database seeded with dummy data!')) 