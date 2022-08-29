from datetime import datetime
from unicodedata import category
from api.models import Expense, ExpenseUser

from rest_framework.views import APIView
from rest_framework.response import Response

from common.utils import verify_expense_date_format


class ExpenseView(APIView):

    authentication_classes = []

    def get(self, request):
        try:
            query_params = dict(request.GET)
            user = query_params.get('user')
            if not user:
                return Response({'message': 'Invalid user!'}, status=404)
            return Response(query_params, status=200)
        except Exception as e:
            print(e)
            return Response({'message': 'Some unexpected error occured!'}, status=500)

    def post(self, request):
        try:
            request_data = dict(request.data)
            amount = request_data.get('amount')
            category = request_data.get('category')
            desc = request_data.get('description', '')
            expense_date = request_data.get('expense_date')
            user = ExpenseUser(contact_number='12345')
            if not amount or not category:
                return Response({'message': 'Amount or Category must be specified!'}, status=400)
            if expense_date:
                if not verify_expense_date_format(expense_date):
                    return Response({'message': 'Expense data is wrong format. Please enter date in dd/mm/yyyy format.'}, status=400)
            else:
                expense_date = datetime.utcnow()

            expense = Expense(amount=amount, category=category, description=desc,
                              expense_date=expense_date, user=user, updated_at=datetime.utcnow())
            expense.save()

            return Response({'message': 'Expense added'}, status=201)
        except Exception as e:
            print(e)
            return Response({'message': 'Some unexpected error occured!'}, status=500)

    def patch(self, request):
        ...

    def delete(self, request):
        ...
