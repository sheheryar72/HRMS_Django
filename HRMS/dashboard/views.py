from django.shortcuts import render
from django.db import connection
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

def dashboard_view(request):
    # print('dashboard called')
    return render(request, 'dashboard.html')

@api_view(['GET'])
def get_all_usermenuforms(request):
    try:
        user_id = request.query_params.get('user_id')
        # print('user_id: ', user_id)
        with connection.cursor() as cursor:
            # cursor.execute("EXEC HR_GetUserMenuAndForms @User_ID=%s", [user_id])
            # cursor.execute("EXEC [ERP_ADMIN].[dbo].HR_GetUserMenuAndForms @User_ID=%s", [user_id])
            print('user_id user_id: ', user_id)
            cursor.execute("EXEC GetUserMenuAndForms @User_ID=%s", [user_id])
            # print('columns columns')
            columns = [col[0] for col in cursor.description]
            # print('columns: ', columns)
            rows = cursor.fetchall()
            # print('rows: ', rows)
            data = [dict(zip(columns, row)) for row in rows]
            # print('data: ', data)
            # print('form data: ', data)
            if not data:
                return Response({'error': 'No data found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


