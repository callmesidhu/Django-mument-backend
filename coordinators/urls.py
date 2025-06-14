from django.urls import path
from .views import AddCoordinatorView, CoordinatorListView

urlpatterns = [
    path("add-player/", AddCoordinatorView.as_view(), name="add-coordinator"),
    path("list/", CoordinatorListView.as_view(), name="list-coordinators"),
]
