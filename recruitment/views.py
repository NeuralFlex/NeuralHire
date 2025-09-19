from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Job, Application, Candidate
from .serializers import JobSerializer, ApplicationSerializer, CandidateSerializer
from .permissions import IsAdminOrCreateOnly
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render

def apply_form(request, job_id):
    return render(request, "apply.html", {"job_id": job_id})


def home(request):
    return HttpResponse("<h1>Welcome to NeuralHire Recruitment Platform</h1>")


class JobViewSet(viewsets.ModelViewSet):
    """Admin CRUD for jobs. Public can view + apply."""
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def get_permissions(self):
        # Public can list, retrieve, and apply
        if self.action in ['list', 'retrieve', 'apply']:
            return [permissions.AllowAny()]
        # Admin/Recruiter only for create/update/delete
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    @csrf_exempt
    def apply(self, request, pk=None):
        """Public endpoint: POST /api/jobs/{id}/apply/"""
        job = self.get_object()
        data = request.data.copy()

        candidate, created = Candidate.objects.get_or_create(
            email=data.get('email'),
            defaults={
                'full_name': data.get('full_name'),
                'phone': data.get('phone'),
                'resume': data.get('resume'),
            }
        )

        if Application.objects.filter(job=job, candidate=candidate).exists():
            return Response(
                {"error": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        app = Application.objects.create(
            job=job,
            candidate=candidate,
            stage="applied"
        )
        return Response(
            {"status": "Application submitted", "application_id": app.id},
            status=status.HTTP_201_CREATED
        )


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related('job', 'candidate').all().order_by('-applied_at')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrCreateOnly]
    filterset_fields = ['stage', 'job']

    def update(self, request, *args, **kwargs):
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
