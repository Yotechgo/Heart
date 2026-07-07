from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import HeartPrediction, PatientUser, AdminUser

# Unregister the default User admin configuration
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Heart predictions table inline for the Patient/User profile page
class HeartPredictionInline(admin.TabularInline):
    model = HeartPrediction
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('name', 'prediction', 'age', 'sex', 'created_at')

@admin.register(PatientUser)
class PatientUserAdmin(BaseUserAdmin):
    inlines = [HeartPredictionInline]

    # Only show standard users (is_staff=False)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

    # Automatically set standard user flags for new creations
    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)

@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    # Only show admin/staff users (is_staff=True)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    # Automatically set full admin (staff & superuser) flags for new creations
    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
            obj.is_superuser = True
        super().save_model(request, obj, form, change)

@admin.register(HeartPrediction)
class HeartPredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "prediction", "age", "sex", "created_at")
    list_filter = ("user", "prediction", "sex", "created_at")
    search_fields = ("user__username", "name", "prediction")