from django.contrib import admin
from api.models import Expense, ExpenseUser
# Register your models here.

admin.site.register(Expense)
admin.site.register(ExpenseUser)
