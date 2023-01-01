from django.contrib import admin

# Register your models here.
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass
