from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'trainer', 'course', 'phone', 'metro', 'created_at')
    list_filter = ('date', 'trainer', 'course')
    search_fields = ('name', 'phone', 'metro')
