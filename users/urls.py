from django.urls import path
from .views import SignupView, ProtectedView, UserUpdateView, AllView, ResetPasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('details/', ProtectedView.as_view(), name='protected'),
    path('update/', UserUpdateView.as_view(), name='update_user'),
    path('all/', AllView.as_view(), name='all-users'),
    path('reset/', ResetPasswordView.as_view(), name='reset_password'),
    
]
