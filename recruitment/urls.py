from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from recruitment.views import home

urlpatterns = [
    path('', home, name='home'),   # root URL
    path('admin/', admin.site.urls),
    path('api/', include('recruitment.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]