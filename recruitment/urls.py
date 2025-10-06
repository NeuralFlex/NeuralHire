from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from recruitment.views import home, JobViewSet, ApplicationViewSet, apply_form
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import NeuralHireTokenObtainPairView

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', home, name='home'),                    # Home page
    path('admin/', admin.site.urls),                # Admin panel
    path('api/', include(router.urls)),            
    path('api/jobs/<int:job_id>/apply/', apply_form, name='apply_form'), 
    path('api/token/', NeuralHireTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
