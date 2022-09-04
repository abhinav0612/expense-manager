from django.urls import path
from api.views import ExpenseView, SummaryView


urlpatterns = [
    path('expense/', ExpenseView.as_view()),
    path('summary/', SummaryView.as_view())
]