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
    description = models.TextField(blank=True)
    responsibility=models.TextField(blank=True)
    requirements=models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=JOB_TYPES, default="full-time")
    location = models.CharField(max_length=100, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title


class CandidateApplication(models.Model):
    STAGES = [
        ('applied', 'Applied'),
        ('phone screen', 'Phone Screen'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ]
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    stage = models.CharField(max_length=20, choices=STAGES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.full_name} - {self.job.title} ({self.stage})"