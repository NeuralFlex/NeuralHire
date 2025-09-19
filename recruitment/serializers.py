from rest_framework import serializers
from .models import Job, Candidate, Application


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    candidate_name = serializers.CharField(source="candidate.full_name", read_only=True)
    candidate_email = serializers.EmailField(source="candidate.email", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "job_title",
            "candidate",
            "candidate_name",
            "candidate_email",
            "stage",
            "applied_at",
        ]
