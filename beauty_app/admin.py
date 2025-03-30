from django.contrib import admin
from .models import Appointment,Contact

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "date", "time", "service", "status")  # ✅ Show status in admin panel
    list_filter = ("status",)  # ✅ Add filter for easy management

admin.site.register(Appointment, AppointmentAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "message", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject")

admin.site.register(Contact, ContactAdmin)
