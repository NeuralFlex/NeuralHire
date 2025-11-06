from rest_framework import serializers
from .models import Job, Candidate, Application
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
    candidate = CandidateSerializer()

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

    def create(self, validated_data):
        candidate_data = validated_data.pop("candidate")
        candidate, _ = Candidate.objects.get_or_create(
            email=candidate_data["email"], defaults=candidate_data
        )
        application = Application.objects.create(candidate=candidate, **validated_data)
        return application

class NeuralHireTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add role info to JWT claims
        token['role'] = 'admin' if user.is_staff else 'user'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Also include role in response payload
        data['role'] = 'admin' if self.user.is_staff else 'user'
        return data
