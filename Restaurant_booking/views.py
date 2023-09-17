from django.views import View
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
from .models import Booking, UserProfile
from .forms import UpdateBookingDetails, EditProfileForm, EditUserForm
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
            {
                "home_active": "",
            }
        )


class MenuView(TemplateView):
    template_name = "menu.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "menu.html",
            {
                "menu_active": "",
            }
        )


class ProfileView(View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user)
        form = EditProfileForm(instance=user_profile)
        user_form = EditUserForm(instance=request.user)
        user_form.fields.pop('password')
        return render(
            request,
            self.template_name,
            {
                "profile": user_profile,
                "EditProfileForm": form,
                "EditUserForm": user_form,
                "updated": False,
            },
        )

    def post(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user)
        form = EditProfileForm(request.POST, instance=user_profile)
        user_form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(
                request, "Profile update failed. Please check the form for errors.")

        return render(
            request,
            self.template_name,
            {
                "profile": user_profile,
                "EditProfileForm": form,
                "EditUserForm": user_form,
                "updated": False,
            },
        )


class ManageBooking(LoginRequiredMixin, TemplateView):
    template_name = "manage_booking.html"
    paginate_by = 6

    def get_queryset(self):
        return Booking.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_list'] = self.get_queryset()
        return context


class OnlineBookingView(View):
    template_name = "online_booking.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "online_booking.html",
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

        return redirect(reverse('manage_booking'))


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

        if request.user != booking.user:
            raise PermissionDenied(
                "You do not have permission to edit this booking.")

        booking_details_form = UpdateBookingDetails(
            request.POST, instance=booking)

        if booking_details_form.is_valid():
            booking.status = 0
            booking_updates = booking_details_form.save()
            return redirect(reverse('manage_booking'))
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
