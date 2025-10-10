from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    JOB_TYPES = [
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
        ("remote", "Remote"),
    ]
    title = models.CharField(max_length=200)
    company_details = models.TextField(blank=True)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=JOB_TYPES, default="full-time")
    location = models.CharField(max_length=100, blank=True)  # onsite, hybrid, remote
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Application(models.Model):
    STAGES = [
        ('applied', 'Applied'),
        ('screening','Screening'),
        ('interview', 'Interview'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, related_name='applications', on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job', 'candidate')  

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title} ({self.stage})"
