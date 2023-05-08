from django.shortcuts import render, get_object_or_404, reverse, redirect
# Import Django generic libary
from django.views import generic, View
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
# Import Booking model from models
from .models import Booking, UserProfile
from .forms import UpdateBookingDetails, EditProfileForm


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

    def post(self, request, user, *args, **kwargs):
        profile = UserProfile.objects.get(user=user)

        edit_profile_form = EditProfileForm(request.POST, instance=profile)

        if edit_profile_form.is_valid():
            profile_updates = edit_profile_form.save()
        else:
            edit_profile_form = EditProfileForm(instance=profile)

        return render(
            request,
            "edit_profile.html",
            {
                "profile": profile,
                'updated': True,
                "Edit_ProfileForm": edit_profile_form,
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


class EditBooking(View):
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
