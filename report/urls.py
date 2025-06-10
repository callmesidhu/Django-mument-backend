from django.urls import path
from .views import SubmitView, DailyReportListView

urlpatterns = [
    path('submit/', SubmitView.as_view(), name='submit_report'),
    path('daily-report/', DailyReportListView.as_view(), name='daily_report'),
    
]
