from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import render
from .models import Job, Application, Candidate
from .serializers import JobSerializer, ApplicationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import NeuralHireTokenObtainPairSerializer


# Homepage
def home(request):
    return render(request, "home.html")


# Candidate apply form page
def apply_form(request, job_id):
    """
    Render a simple form page to apply for a specific job.
    """
    return render(request, "apply.html", {"job_id": job_id})


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'apply']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def close(self, request, pk=None):
        """Mark job as closed."""
        job = self.get_object()
        job.is_open = False
        job.save()
        return Response({"message": "Job closed successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def open(self, request, pk=None):
        """Reopen a closed job."""
        job = self.get_object()
        job.is_open = True
        job.save()
        return Response({"message": "Job reopened successfully"}, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def apply(self, request, pk=None):
        job = self.get_object()

        if not job.is_open:
            return Response(
                {"error": "This job is closed for applications."},
                status=status.HTTP_400_BAD_REQUEST
            )

        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone = request.data.get("phone", "")
        experience = request.data.get("experience", None)
        resume_file = request.FILES.get("resume")

        # Validate required fields
        if not full_name or not email or not resume_file:
            return Response(
                {"error": "full_name, email, and resume are required to proceed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or update candidate
        candidate, created = Candidate.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name, "phone": phone, "resume": resume_file}
        )

        if not created:
            candidate.full_name = full_name
            candidate.phone = phone
            candidate.experience = experience
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
    
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['stage', 'job']

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.select_related('job', 'candidate').all()

        if user.is_superuser or user.is_staff:
            return queryset.order_by('-applied_at')

        # For non-staff users, filter by email
        return queryset.filter(candidate__email=user.email).order_by('-applied_at')

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


class NeuralHireTokenObtainPairView(TokenObtainPairView):
    serializer_class = NeuralHireTokenObtainPairSerializer
