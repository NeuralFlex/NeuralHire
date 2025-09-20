from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from .models import Job, Application, Candidate
from .serializers import JobSerializer, ApplicationSerializer
from .permissions import IsAdminOrCreateOnly


# Optional homepage
def home(request):
    return render(request, "home.html")


# Optional frontend form page
def apply_form(request, job_id):
    return render(request, "apply.html", {"job_id": job_id})

class JobViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD for jobs.
    Public can view jobs and apply.
    """
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    parser_classes = [MultiPartParser, FormParser]  # for file uploads

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'apply']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def apply(self, request, pk=None):
        """
        Public endpoint: POST /api/jobs/{id}/apply/
        Handles candidate creation and application.
        """
        job = self.get_object()

        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone = request.data.get("phone", "")
        resume_file = request.FILES.get("resume")

        # Validate required fields
        if not full_name or not email or not resume_file:
            return Response(
                {"error": "full_name, email, and resume are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or update candidate
        candidate, created = Candidate.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name, "phone": phone, "resume": resume_file}
        )

        if not created:
            # Update existing candidate
            candidate.full_name = full_name
            candidate.phone = phone
            candidate.resume = resume_file
            candidate.save()

        # Check if already applied
        if Application.objects.filter(job=job, candidate=candidate).exists():
            return Response(
                {"error": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create application
        app = Application.objects.create(job=job, candidate=candidate, stage="applied")

        return Response(
            {
                "status": "Application submitted",
                "application_id": app.id,
                "candidate": candidate.full_name,
                "job": job.title
            },
            status=status.HTTP_201_CREATED
        )


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Admin-only: manage candidate applications
    """
    queryset = Application.objects.select_related('job', 'candidate').all().order_by('-applied_at')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrCreateOnly]
    filterset_fields = ['stage', 'job']

    def update(self, request, *args, **kwargs):
        """
        Restrict updates to only the 'stage' field.
        """
        instance = self.get_object()
        stage = request.data.get("stage")
        if not stage:
            return Response(
                {"error": "You can only update the 'stage' field."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.stage = stage
        instance.save()
        return Response(self.get_serializer(instance).data)
