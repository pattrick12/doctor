from django import forms
from .models import Customer, Pet, Appointment, VaccinationRecord

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_number', 'address', 'email']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['customer', 'name', 'species', 'breed', 'age', 'gender', 'notes']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'customer', 'treating_doctor', 'appointment_date', 'reason', 'diagnosis', 'prescription', 'additional_notes', 'status']

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['pet', 'customer', 'treating_doctor', 'vaccine_name', 'vaccination_date', 'next_due_date', 'notes', 'additional_notes']