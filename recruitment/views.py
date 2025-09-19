# jobs/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, CandidateApplication
from .serializers import JobSerializer, CandidateApplicationSerializer
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to NeuralFlex HR Recruitment System</h1>")


class JobViewSet(viewsets.ModelViewSet):
    """Public job listing and admin CRUD."""
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.AllowAny]
    )
    def apply(self, request, pk=None):
        """Public endpoint: POST /api/jobs/{id}/apply/ with form-data (full_name, email, resume)"""
        job = self.get_object()
        data = request.data.copy()
        data['job'] = job.id

        serializer = CandidateApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # TODO: trigger email notification here (send confirmation to candidate)
            return Response({'status': 'Application submitted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    """Protected: list and update application stage. Keep default perms (IsAuthenticated)."""
    queryset = CandidateApplication.objects.select_related('job').all().order_by('-applied_at')
    serializer_class = CandidateApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['stage', 'job']

    def partial_update(self, request, *args, **kwargs):
        # Only allow updating 'stage'
        if 'stage' not in request.data:
            return Response(
                {"error": "You can only update the 'stage' field."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)
