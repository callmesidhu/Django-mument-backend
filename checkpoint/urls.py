from django.urls import path
from .views import AddCheckpointView, ShowCheckpointView

urlpatterns = [
    path('add-checkpoint/', AddCheckpointView.as_view(), name='add-checkpoint'),
    path('show-checkpoint/', ShowCheckpointView.as_view(), name='show-checkpoint'),
]
