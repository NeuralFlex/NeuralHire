from django.contrib import admin
from .models import Job, Candidate, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_open", "created_at")
    list_filter = ( "is_open", "location")
    search_fields = ("title", "description", "department")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at")
    search_fields = ("full_name", "email")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "stage", "applied_at")
    list_filter = ("stage", "job")
    search_fields = ("candidate__full_name", "candidate__email")
