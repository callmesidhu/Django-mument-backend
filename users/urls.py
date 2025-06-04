from django.urls import path
from .views import SignupView, ProtectedView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('details/', ProtectedView.as_view(), name='protected'),
]
