from django.urls import path
from .views import AddCoordinatorView, ListCoordinatorsView

urlpatterns = [
    path("add-player/", AddCoordinatorView.as_view(), name="add-coordinator"),
    path("list/", ListCoordinatorsView.as_view(), name="list-coordinators"),
]
