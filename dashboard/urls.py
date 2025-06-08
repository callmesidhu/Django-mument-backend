from django.urls import path
from .views import DashboardView, DashboardCreateView
urlpatterns = [
    path('list/', DashboardView.as_view(), name='dashboard_list'),
    path('create/', DashboardCreateView.as_view(), name='dashboard_create'),  
]
