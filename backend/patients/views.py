from django.shortcuts import render, redirect, HttpResponse
from rest_framework import viewsets
from .models import Customer, Pet, Appointment, VaccinationRecord
from .serializers import CustomerSerializer, PetSerializer, AppointmentSerializer, VaccinationRecordSerializer
from .forms import CustomerForm, PetForm

# API Views
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer


def customers(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

# Template Views
def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'register_customer.html', {'form': form})

def register_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'register_pet.html', {'form': form})

def hello(request):
    return HttpResponse("Hello, world. You're at the patients index.")