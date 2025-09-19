from rest_framework import serializers
from .models import Job, CandidateApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    
class CandidateApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    class Meta:
        model = CandidateApplication
        fields = ["id", "job", "job_title", "full_name", "email", "resume", "stage", "applied_at"]
