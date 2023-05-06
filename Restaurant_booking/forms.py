from .models import Booking, UserProfile
from django import forms
from django.forms import ModelForm, CharField, TextInput


class BookingDetails(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('booking_date', 'booking_time', 'guest_count',
                  'special_requests',)
