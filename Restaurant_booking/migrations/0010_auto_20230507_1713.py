# Generated by Django 3.2.18 on 2023-05-07 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant_booking', '0009_remove_booking_allergies'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='special_requests',
            new_name='booking_comments',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]