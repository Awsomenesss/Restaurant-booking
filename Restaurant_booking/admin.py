from django.contrib import admin
# Import Booking model from models.py
from .models import Booking, UserProfile


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ('status', 'booking_time', 'booking_date')
    readonly_fields = ('booking_id',)
    list_display = ('booking_id', 'user', 'booking_date', 'booking_time', 'guest_count',
                    'status', 'created_on',)
    search_fields = ('booking_id', 'user')
    actions = ['approve_booking']

    def approve_booking(self, queryset):
        queryset.update(approve_booking=True)


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name',
                    'phone_number', 'email',)
    search_fields = ('user', 'first_name', 'last_name',
                     'phone_number')
