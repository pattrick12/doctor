from django import forms
from .models import Customers, Pets, Appointments, VaccinationRecords
from django_select2.forms import Select2Widget
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'contact_number', 'address', 'email']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pets
        fields = ['customer', 'name', 'species', 'breed', 'age', 'gender', 'notes']
        widgets = {
            'customer': Select2Widget,
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['customer', 'pet', 'appointment_date', 'reason', 'status', 'appointment_type', 'treating_doctor', 'diagnosis', 'prescription', 'additional_notes']
        widgets = {
            'customer': Select2Widget,
            'pet': Select2Widget,
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        if edit_mode:
            self.fields['customer'].disabled = True
            self.fields['pet'].disabled = True
        self.fields['pet'].queryset = Pets.objects.none()

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['pet'].queryset = Pets.objects.filter(customer_id=customer_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['pet'].queryset = self.instance.customer.pets_set.order_by('name')
class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecords
        fields = ['customer', 'pet', 'treating_doctor', 'vaccine_name', 'vaccination_date', 'next_due_date', 'notes', 'additional_notes']
        widgets = {
            'customer': Select2Widget,
            'pet': Select2Widget,
            'vaccination_date': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        if edit_mode:
            self.fields['customer'].disabled = True
            self.fields['pet'].disabled = True
        self.fields['pet'].queryset = Pets.objects.none()

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['pet'].queryset = Pets.objects.filter(customer_id=customer_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['pet'].queryset = self.instance.customer.pets_set.order_by('name')

class CustomerSearchForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customers.objects.all(), widget=Select2Widget)

