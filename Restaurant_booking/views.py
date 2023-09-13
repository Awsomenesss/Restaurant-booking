from django.shortcuts import render, get_object_or_404, reverse, redirect
# Import Django generic libary
from django.views import generic, View
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
# Import Booking model from models
from .models import Booking, UserProfile
from .forms import UpdateBookingDetails, EditProfileForm

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied


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


class CreateProfile(View):
    template_name = "create_profile.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "create_profile.html",
        )

    def post(self, request):
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        tele = request.POST.get("phone_number")

        CreateUserProfile = UserProfile.objects.create(
            first_name=f_name,
            last_name=l_name,
            phone_number=tele,
            user=request.user,
        )

        CreateUserProfile.save()

        return redirect(reverse('home'))


class EditProfile(View):
    model = UserProfile
    template_name = "edit_profile.html"
    context_object_name = 'edit_profile'

    def get(self, request, user, *args, **kwargs):
        profile = UserProfile.objects.filter(user=user).first()
        if profile is None:
            return redirect(reverse('create_profile'))

        return render(
            request,
            "edit_profile.html",
            {
                "profile": profile,
                "updated": False,
                "Edit_ProfileForm": EditProfileForm,
                "edit_profile_active": "custom-red",
            },
        )


class ManageBooking(generic.ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = "manage_booking.html"
    paginate_by = 6
    extra_context = {
        "manage_booking_active": "custom-red"
    }

    def get_queryset(self):
        return Booking.objects.filter(user_id=self.request.user)


class OnlineBookingView(View):
    template_name = "online_booking.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "online_booking.html",
            {
                "online_booking_active": "custom-red",
            }
        )

    def post(self, request):
        date = request.POST.get("date")
        time = request.POST.get("time")
        guest_count = request.POST.get("guest_count")
        comments = request.POST.get("comments")

        online_booking = Booking.objects.create(
            booking_date=date,
            booking_time=time,
            guest_count=guest_count,
            user=request.user,
            booking_comments=comments
        )

        online_booking.save()

        return redirect(reverse('home'))


class UserOwnsBookingMixin:
    def user_owns_booking(self, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        if self.request.user == booking.user:
            return booking
        else:
            raise Http404(
                "Booking does not exist or you do not have permission to access it.")

    def dispatch(self, request, *args, **kwargs):
        booking_id = kwargs.get('booking_id')
        booking = self.user_owns_booking(booking_id)
        self.booking = booking
        return super().dispatch(request, *args, **kwargs)


class EditBooking(UserOwnsBookingMixin, View):
    model = Booking
    template_name = "edit_booking.html"
    context_object_name = 'edit_booking'

    def get(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=booking_id)

        return render(
            request,
            "edit_booking.html",
            {
                "booking": booking,
                "updated": False,
                "Update_BookingDetails": UpdateBookingDetails(instance=booking)
            },
        )

    def post(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=booking_id)

        # Check if the logged-in user owns the booking
        if request.user != booking.user:
            raise PermissionDenied(
                "You do not have permission to edit this booking.")

        booking_details_form = UpdateBookingDetails(
            request.POST, instance=booking)

        if booking_details_form.is_valid():
            booking.status = 0
            booking_updates = booking_details_form.save()
        else:
            booking_details_form = UpdateBookingDetails(instance=booking)

        return render(
            request,
            "edit_booking.html",
            {
                "booking": booking,
                'updated': True,
                "Update_BookingDetails": booking_details_form,
            },
        )


class DeleteBooking(DeleteView):
    model = Booking
    pk_url_kwarg = "booking_id"
    success_url = reverse_lazy("manage_booking")
    template_name = "delete_booking.html"
