from django.urls import path
from api.views import ExpenseView, SummaryView, AnalysisView, TrendsView


urlpatterns = [
    path('expense/', ExpenseView.as_view()),
    path('summary/', SummaryView.as_view()),
    path('trend/', TrendsView.as_view()),
    path('analysis/', AnalysisView.as_view())
]