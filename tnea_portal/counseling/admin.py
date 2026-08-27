from django.contrib import admin
from .models import College, Branch, Cutoff, StudentProfile, Application


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('college_code', 'name', 'place', 'district', 'college_type')
    search_fields = ('college_code', 'name', 'district')
    list_filter = ('college_type', 'district')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Cutoff)
class CutoffAdmin(admin.ModelAdmin):
    list_display = ('college', 'branch', 'community', 'cutoff_mark', 'year')
    list_filter = ('community', 'year', 'branch')
    search_fields = ('college__name', 'branch__name')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'phone', 'cutoff_mark')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'cutoff', 'status', 'created_at')
    list_filter = ('status', 'created_at')