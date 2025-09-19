from django.contrib import admin
from .models import Job, CandidateApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','location','is_open','created_at')
    list_filter = ('is_open',)
    search_fields = ('title','description')


@admin.register(CandidateApplication)
class CandidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name','email','job','stage','applied_at')
    list_filter = ('stage','job')
    search_fields = ('full_name','email')