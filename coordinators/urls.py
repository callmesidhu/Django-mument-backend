from django.urls import path
from .views import AddCoordinatorView, CoordinatorListView, CoordinatorPlayerDetailsView

urlpatterns = [
    path("add-player/", AddCoordinatorView.as_view(), name="add-coordinator"),
    path("list/", CoordinatorListView.as_view(), name="list-coordinators"),
    path("players-details/",CoordinatorPlayerDetailsView.as_view(), name="list-players-details")
]
