from django.urls import path

from panel import views

app_name = 'panel'

urlpatterns = [
    path('login/', views.PanelLoginView.as_view(), name='login'),
    path('logout/', views.PanelLogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('api/appointments/', views.appointments_api, name='appointments-api'),
    path('api/appointments/<int:pk>/approve/', views.appointment_approve, name='appointment-approve'),
    path('api/appointments/<int:pk>/reject/', views.appointment_reject, name='appointment-reject'),
    path('blogs/', views.blog_list, name='blog-list'),
    path('blogs/new/', views.blog_create, name='blog-create'),
    path('blogs/<int:pk>/edit/', views.blog_edit, name='blog-edit'),
    path('blogs/<int:pk>/delete/', views.blog_delete, name='blog-delete'),
    path('schedules/', views.schedules, name='schedules'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact-detail'),
    path('users/', views.users_list, name='users'),
    path('users/new/', views.user_create, name='user-create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user-edit'),
]
