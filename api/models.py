from datetime import datetime
from operator import mod
from django.db import models

# Create your models here.


class BaseModel(models.Model):

    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField()


class ExpenseUser(models.Model):
    user_id = models.IntegerField(null=False, primary_key=True)


class Expense(BaseModel):

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    expense_date = models.DateField(null=False)
    category = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(to=ExpenseUser, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, default='')
    unique_message_id = models.CharField(
        max_length=256, null=False, default='')
