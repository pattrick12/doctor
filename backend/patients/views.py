from django.shortcuts import render, redirect, HttpResponse
from rest_framework import viewsets
from .models import Customers, Pets, Appointments, VaccinationRecords
from .serializers import CustomerSerializer, PetSerializer, AppointmentSerializer, VaccinationRecordSerializer
from .forms import CustomerForm, PetForm, AppointmentForm, VaccinationRecordForm, CustomerSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse


def get_pets_by_customer(request):
    customer_id = request.GET.get('customer_id')
    pets = Pets.objects.filter(customer_id=customer_id).values('id', 'name')
    return JsonResponse({'pets': list(pets)})


# API Views
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pets.objects.all()
    serializer_class = PetSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer


class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecords.objects.all()
    serializer_class = VaccinationRecordSerializer


def customer_list(request):
    customers = Customers.objects.all()
    return render(request, 'customers.html', {'customers': customers})


# Template Views
def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
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


from django.utils import timezone


def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})


def record_vaccination(request):
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vaccinations_list')
    else:
        form = VaccinationRecordForm()
    return render(request, 'record_vaccination.html', {'form': form})


def customer_search(request):
    form = CustomerSearchForm()
    query = request.GET.get('q')
    if query:
        customers = Customers.objects.filter(name__icontains=query)
    else:
        customers = Customers.objects.all()
    return render(request, 'getcustomers.html', {'form': form, 'customers': customers})


def pet_list(request):
    query = request.GET.get('q')
    if query:
        pets = Pets.objects.filter(name__icontains=query)
    else:
        pets = Pets.objects.all()
    return render(request, 'pets.html', {'pets': pets})


def customer_detail(request, customer_id):
    customer = Customers.objects.get(id=customer_id)
    appointments = Appointments.objects.filter(customer=customer)
    vaccination_records = VaccinationRecords.objects.filter(customer=customer)
    pets = Pets.objects.filter(customer=customer)
    return render(request, 'customer_detail.html', {
        'customer': customer,
        'pets': pets,
        'appointments': appointments,
        'vaccination_records': vaccination_records
    })


def pet_detail(request, pet_id):
    pet = Pets.objects.get(id=pet_id)
    appointments = Appointments.objects.filter(pet=pet)
    vaccination_records = VaccinationRecords.objects.filter(pet=pet)
    return render(request, 'pet_detail.html', {
        'pet': pet,
        'appointments': appointments,
        'vaccination_records': vaccination_records
    })


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customers, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})


def edit_pet(request, pet_id):
    pet = get_object_or_404(Pets, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'edit_pet.html', {'form': form})


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            appointment.delete()
            return redirect('appointments_list')
        form = AppointmentForm(request.POST, instance=appointment, edit_mode=True)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm(instance=appointment, edit_mode=True)
    return render(request, 'edit_appointment.html', {'form': form})


def edit_vaccination(request, vaccination_id):
    vaccination = get_object_or_404(VaccinationRecords, id=vaccination_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            vaccination.delete()
            return redirect('vaccinations_list')
        form = VaccinationRecordForm(request.POST, instance=vaccination, edit_mode=True)
        if form.is_valid():
            form.save()
            return redirect('vaccinations_list')
    else:
        form = VaccinationRecordForm(instance=vaccination, edit_mode=True)
        form.fields['customer'].disabled = True
        form.fields['pet'].disabled = True
    return render(request, 'edit_vaccination.html', {'form': form})


def calendar_view(request):
    return render(request, 'calendar.html')


def hello(request):
    return render(request, 'dashboard.html')


def vaccination_detail(request, vaccination_id):
    vaccination = get_object_or_404(VaccinationRecords, id=vaccination_id)
    return render(request, 'vaccination_detail.html', {'vaccination': vaccination})


def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})


def appointments_list(request):
    today = timezone.now().date()
    todays_appointments = Appointments.objects.filter(appointment_date=today)
    all_appointments = Appointments.objects.all().order_by('appointment_date')
    return render(request, 'appointments_list.html', {
        'todays_appointments': todays_appointments,
        'all_appointments': all_appointments
    })


def vaccinations_list(request):
    today = timezone.now().date()
    todays_vaccinations = VaccinationRecords.objects.filter(vaccination_date=today)
    all_vaccinations = VaccinationRecords.objects.all().order_by('vaccination_date')
    return render(request, 'vaccinations_list.html', {
        'todays_vaccinations': todays_vaccinations,
        'all_vaccinations': all_vaccinations
    })
