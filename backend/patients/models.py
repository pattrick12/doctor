

# Create your models here.
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import date
from django.core.validators import MaxValueValidator

class Customers(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

from django.db import models

class Pets(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    ]

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True, null=True)
    age_years = models.PositiveIntegerField(blank=True, null=True)
    age_months = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(11)])
    age_days = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(28)])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unknown')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            years = today.year - self.date_of_birth.year
            months = today.month - self.date_of_birth.month
            days = today.day - self.date_of_birth.day
            if days < 0:
                months -= 1
                days += 30
            if months < 0:
                years -= 1
                months += 12
            return f"{years} years, {months} months, {days} days"
        elif self.age_years is not None or self.age_months is not None or self.age_days is not None:
            return f"{self.age_years or 0} years, {self.age_months or 0} months, {self.age_days or 0} days"
        return None
class Users(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Doctor')
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ('Walk-in', 'Walk-in'),
        ('Future Scheduled', 'Future Scheduled'),
    ]

    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    treating_doctor = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='Future Scheduled')

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.appointment_date}"

    def delete(self, *args, **kwargs):
        billing = Billing.objects.filter(object_id=self.id,
                                         content_type=ContentType.objects.get_for_model(Appointments)).first()
        if billing:
            if billing.payment_status == 'Paid':
                billing.payment_status = 'Refunded'
            elif billing.payment_status == 'Pending':
                billing.payment_status = 'Cancelled'
            billing.save()
        super().delete(*args, **kwargs)

class VaccinationRecords(models.Model):
    pet= models.ForeignKey(Pets, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    treating_doctor = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    vaccine_name = models.CharField(max_length=100)
    vaccination_date = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Vaccination for {self.pet.name} on {self.vaccination_date}"

    def delete(self, *args, **kwargs):
        billing = Billing.objects.filter(object_id=self.id,
                                         content_type=ContentType.objects.get_for_model(VaccinationRecords)).first()
        if billing:
            if billing.payment_status == 'Paid':
                billing.payment_status = 'Refunded'
            elif billing.payment_status == 'Pending':
                billing.payment_status = 'Cancelled'
            billing.save()
        super().delete(*args, **kwargs)
class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    pet= models.ForeignKey(Pets, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)

    object_id = models.PositiveIntegerField(null=  True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Billing for {self.pet.name} - {self.total_amount}"