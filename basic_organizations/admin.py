from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganisationAdmin(admin.ModelAdmin):
    pass
