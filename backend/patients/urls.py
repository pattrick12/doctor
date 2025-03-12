from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PetViewSet, AppointmentViewSet, VaccinationRecordViewSet, register_customer, register_pet, hello
from . import views


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'pets', PetViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'vaccination-records', VaccinationRecordViewSet)

urlpatterns = [
    path('', views.hello, name='hello'),
    path('register_customer/', register_customer, name='register_customer'),
    path('register_pet/', register_pet, name='register_pet'),
    path('all_customers/', views.customer_list, name='customer_list'),
    path('api/', include(router.urls)),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('record_vaccination/', views.record_vaccination, name='record_vaccination'),
    path('customers/', views.customer_search, name='customer_search'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),  # Add this line
    path('calendar/', views.calendar_view, name='calendar_view')
]
urlpatterns += [
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('pets/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
]
urlpatterns += [
    path('appointments/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    path('vaccinations/<int:vaccination_id>/edit/', views.edit_vaccination, name='edit_vaccination'),
    path('vaccination_detail/<int:vaccination_id>/', views.vaccination_detail, name='vaccination_detail'),
    path('appointment_detail/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments_all/', views.appointments_list, name='appointments_list'),
    path('vaccinations_all/', views.vaccinations_list, name='vaccinations_list'),
    path('ajax/get_pets_by_customer/', views.get_pets_by_customer, name='get_pets_by_customer'),
]