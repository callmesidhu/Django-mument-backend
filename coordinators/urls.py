from django.urls import path
from .views import AddCoordinatorView

urlpatterns = [
    path('add/', AddCoordinatorView.as_view(), name='add_coordinator'),
]
