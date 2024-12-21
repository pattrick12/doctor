from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PetViewSet, AppointmentViewSet, VaccinationRecordViewSet, register_customer, register_pet, hello

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'pets', PetViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'vaccination-records', VaccinationRecordViewSet)

urlpatterns = [
    path('', hello, name='hello'),
    path('register_customer/', register_customer, name='register_customer'),
    path('register_pet/', register_pet, name='register_pet'),
    path('api/', include(router.urls)),
]