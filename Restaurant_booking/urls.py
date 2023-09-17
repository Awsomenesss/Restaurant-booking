from django.urls import path
from . import views

from .views import ProfileView


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path(
        'online_booking/',
        views.OnlineBookingView.as_view(),
        name='online_booking'
    ),
    path('profile/', ProfileView.as_view(), name='profile'),
    path(
        'manage_booking/',
        views.ManageBooking.as_view(),
        name='manage_booking'
    ),
    path(
        'edit_booking/<str:booking_id>/',
        views.EditBooking.as_view(),
        name='edit_booking'
    ),
    path(
        'delete_booking/<str:booking_id>/',
        views.DeleteBooking.as_view(),
        name='delete_booking'
    ),
]
