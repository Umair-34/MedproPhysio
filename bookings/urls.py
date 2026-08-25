from django.urls import path

from bookings import views

app_name = 'bookings'

urlpatterns = [
    path('services/', views.service_list, name='service-list'),
    path('practitioners/', views.practitioner_list, name='practitioner-list'),
    path('slots/', views.available_slots, name='available-slots'),
    path('appointments/', views.create_booking, name='create-booking'),
    path('appointments/<uuid:token>/', views.appointment_detail, name='appointment-detail'),
    path('appointments/<uuid:token>/cancel/', views.cancel_booking, name='cancel-booking'),
]
