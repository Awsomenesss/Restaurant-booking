# Generated by Django 3.2.18 on 2023-05-01 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('booking_date', models.DateField(auto_now=True)),
                ('booking_time', models.TimeField(auto_now=True)),
                ('booking_comments', models.TextField(blank=True, max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('guest_count', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, 'Booking Requested'), (1, 'Booking Accepted')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-booking_date'],
            },
        ),
    ]