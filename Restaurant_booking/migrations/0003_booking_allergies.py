# Generated by Django 3.2.18 on 2023-05-01 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant_booking', '0002_auto_20230501_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='allergies',
            field=models.CharField(blank=True, choices=[('milk', 'Milk'), ('eggs', 'Eggs'), ('fish', 'Fish (e.g., bass, flounder, cod)'), ('shellfish', 'Crustacean shellfish (e.g., crab, lobster, shrimp)'), ('nuts', 'Tree nuts (e.g., almonds, walnuts, pecans)'), ('peanuts', 'Peanuts'), ('wheat', 'Wheat'), ('soy', 'Soybeans'), ('sesame', 'Sesame')], default='', max_length=100),
        ),
    ]
