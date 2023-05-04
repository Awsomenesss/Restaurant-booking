from django.shortcuts import render, get_object_or_404
# Import Django generic libary
from django.views import generic, View
from django.views.generic import TemplateView
# Import Booking model from models
from .models import Booking, UserProfile


class HomeView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
            {
                "home_active",
            }
        )


