from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Job, Application, Candidate
from .serializers import JobSerializer, ApplicationSerializer
from .permissions import IsAdminOrCreateOnly


def home(request):
    return HttpResponse("<h1>Welcome to NeuralHire Recruitment Platform</h1>")


def apply_form(request, job_id):
    return render(request, "apply.html", {"job_id": job_id})


class JobViewSet(viewsets.ModelViewSet):
    """Admin CRUD for jobs. Public can view + apply."""
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'apply']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def apply(self, request, pk=None):
        """Public endpoint: POST /api/jobs/{id}/apply/"""
        job = self.get_object()
        data = request.data

        # Handle file upload
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({"error": "Resume file is required."}, status=status.HTTP_400_BAD_REQUEST)

        candidate, created = Candidate.objects.get_or_create(
            email=data.get('email'),
            defaults={
                'full_name': data.get('full_name'),
                'phone': data.get('phone', ''),
                'resume': resume_file,
            }
        )

        if not created:
            candidate.resume = resume_file
            candidate.save()


        if Application.objects.filter(job=job, candidate=candidate).exists():
            return Response({"error": "You have already applied for this job."}, status=status.HTTP_400_BAD_REQUEST)


        app = Application.objects.create(job=job, candidate=candidate, stage='applied')

        return Response({"status": "Application submitted", "application_id": app.id}, status=status.HTTP_201_CREATED)


class ApplicationViewSet(viewsets.ModelViewSet):
    """Admin-only: manage candidate applications."""
    queryset = Application.objects.select_related('job', 'candidate').all().order_by('-applied_at')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrCreateOnly]  
    filterset_fields = ['stage', 'job']

    def update(self, request, *args, **kwargs):
        """Restrict updates to only the 'stage' field."""
        instance = self.get_object()
        stage = request.data.get("stage")
        if not stage:
            return Response({"error": "You can only update the 'stage' field."}, status=status.HTTP_400_BAD_REQUEST)

        instance.stage = stage
        instance.save()
        return Response(self.get_serializer(instance).data)
