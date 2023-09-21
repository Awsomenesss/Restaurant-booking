from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Booking, UserProfile
from .views import HomeView, MenuView, ProfileView, ManageBooking, OnlineBookingView, UserOwnsBookingMixin
from django.http import QueryDict
from .models import Booking


class MyViewTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='test1', password='Hi2023!123')

        # Create a request factory
        self.booking = Booking.objects.create(
            user=self.user,
            booking_date='2023-09-19',
            booking_time='16:00:00',
            booking_comments='Test comment',
            guest_count=2,
            status=0
        )
        self.factory = RequestFactory()

    def test_home_view(self):
        request = self.factory.get(reverse('home'))
        request.user = self.user

        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_menu_view(self):

        request = self.factory.get(reverse('menu'))
        request.user = self.user

        response = MenuView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):

        request = self.factory.get(reverse('profile'))
        request.user = self.user

        response = ProfileView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_manage_booking_view(self):
        request = self.factory.get(reverse('manage_booking'))
        request.user = self.user
        response = ManageBooking.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_online_booking_view_get(self):

        request = self.factory.get(reverse('online_booking'))
        request.user = self.user

        response = OnlineBookingView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_online_booking_view_post(self):

        request = self.factory.post(reverse('online_booking'))
        request.user = self.user

        post_data = QueryDict(mutable=True)
        post_data['date'] = '2023-09-18'
        post_data['time'] = '7:00 PM'
        post_data['guest_count'] = '4'
        post_data['comments'] = 'Test comment'

        request.POST = post_data

        response = OnlineBookingView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('manage_booking'))

    def test_user_owns_booking_mixin(self):

        self.client.login(username='test1', password='Hi2023!123')

        request = self.factory.get(reverse('manage_booking'))
        self.assertEqual(response.status_code, 200)
