# Generated by Django 5.1.4 on 2025-03-19 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_remove_pets_age_pets_age_months_pets_age_years_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pets',
            name='age_days',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(28)]),
        ),
        migrations.AlterField(
            model_name='pets',
            name='age_months',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(11)]),
        ),
    ]
