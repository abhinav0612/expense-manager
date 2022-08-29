from django.urls import path
from api.views import ExpenseView


urlpatterns = [
    path('expense/', ExpenseView.as_view())
]