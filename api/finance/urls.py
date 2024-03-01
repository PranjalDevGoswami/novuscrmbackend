from django.urls import path
from .views import FinanceDashboardAPIView, AllFinanceTeamDataAPIView

urlpatterns = [
    path('finance-team/', AllFinanceTeamDataAPIView.as_view(), name='finance-team-list'),
    path('finance-dashboard/<str:project_code>/', FinanceDashboardAPIView.as_view(), name='finance_dashboard'),
]


