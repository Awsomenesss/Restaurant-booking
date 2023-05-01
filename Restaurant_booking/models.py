import uuid
from django.db import models
# Import Django authentication user system
from django.contrib.auth.models import User
# Create your models here.
ALLERGY_CHOICES = [('milk', 'Milk'), ('eggs', 'Eggs'), ('fish', 'Fish (e.g., bass, flounder, cod)'), ('shellfish', 'Crustacean shellfish (e.g., crab, lobster, shrimp)'),
                   ('nuts', 'Tree nuts (e.g., almonds, walnuts, pecans)'), ('peanuts', 'Peanuts'), ('wheat', 'Wheat'), ('soy', 'Soybeans'), ('sesame', 'Sesame'),]
STATUS = ((0, "Booking Requested"), (1, "Booking Accepted"))


class Booking(models.Model):
    booking_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bookings")
    booking_date = models.DateField(auto_now=True)
    booking_time = models.TimeField(auto_now=True)
    booking_comments = models.TextField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    guest_count = models.IntegerField()
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-booking_date']


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return str(self.user)
