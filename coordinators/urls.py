from django.urls import path
from .views import AddCoordinatorView, CoordinatorListView

urlpatterns = [
    path('add/', AddCoordinatorView.as_view(), name='add_coordinator'),
    path('list/', CoordinatorListView.as_view(), name='list_coordinators'),
]
