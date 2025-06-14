from django.urls import path
from .views import SignupView, ProtectedView, UserUpdateView, AllView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('details/', ProtectedView.as_view(), name='protected'),
    path('update/', UserUpdateView.as_view(), name='update_user'),
    path('all/', AllView.as_view(), name='all-users'),
    
]
