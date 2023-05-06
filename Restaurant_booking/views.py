from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic import TemplateView
from .models import Booking, UserProfile
from .forms import BookingDetails


class HomeView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
            {
                "home_active": "custom-red",
            }
        )


class MenuView(TemplateView):
    template_name = "menu.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "menu.html",
            {
                "menu_active": "custom-red",
            }
        )


class ContactView(TemplateView):
    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "contact.html",
            {
                "contact_active": "custom-red",
            }
        )


class MyBooking(View):
    model = Booking
    template_name = "Mybooking.html"
    context_object_name = 'booking'

    def get(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=booking_id)

        return render(
            request,
            "Mybooking.html",
            {
                "booking": booking,
                "updated": False,
                "Update_BookingDetails": UpdateBookingDetails(instance=booking)
            },
        )
