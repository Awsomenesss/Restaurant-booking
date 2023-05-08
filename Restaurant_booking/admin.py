from django.contrib import admin
# Import Booking model from models.py
from .models import Booking, UserProfile


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ('status', 'booking_time', 'booking_date')
    readonly_fields = ('booking_id',)
    list_display = (
        'booking_id', 'user', 'booking_date', 'booking_time', 'guest_count',
        'status', 'created_on')
    search_fields = ('booking_id', 'user')
    actions = ['accept_booking']

    def accept_booking(self, request, queryset):
        queryset.update(status=1)
        self.message_user(request, "Selected bookings have been accepted.")

    accept_booking.short_description = "Accept selected bookings"


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number')
    search_fields = ('user', 'phone_number')
