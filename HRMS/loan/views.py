from django.shortcuts import render
from .models import HR_Loans
from .serializers import HR_Loans_Serializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

def loan_view(request):
    return render(request, 'loan.html')

@api_view(['GET'])
def loan_list(request):
    try:
        loans = HR_Loans.objects.all()
        loan_list = []
        for loan in loans:
            item = {
                "Loan_ID": loan.Loan_ID,
                "Loan_Date": loan.Loan_Date,
                "Loan_Type": loan.Loan_Type,
                "Loan_Amount": loan.Loan_Amount,
                "Loan_Ded_Amt": loan.Loan_Ded_Amt,
                "Loan_Ded_NoofMnth": loan.Loan_Ded_NoofMnth,
                "Remarks": loan.Remarks,
                "Loan_Status": loan.Loan_Status,
                "Previous_Ded_Amount": loan.Previous_Ded_Amount,
                "FYID": loan.FYID.FYID,
                "Emp_ID": loan.Emp_ID.Emp_ID,
                "Emp_Name": loan.Emp_ID.Emp_Name
            }
            loan_list.append(item)
        # loans_serializer = HR_Loans_Serializer(loans, many=True)
        return Response(loan_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def loan_byid(request, pk):
    try:
        try:
            loan = HR_Loans.objects.get(pk=pk)
            loan_serializer = HR_Loans_Serializer(loan)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(loan_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def add_loan(request):
    try:
        data = request.data
        print('request: ', request.data)
        loan_serializer = HR_Loans_Serializer(data=data)
        if loan_serializer.is_valid():
            loan_serializer.save()
            return Response(loan_serializer.data, status=status.HTTP_200_OK)
        return Response({'error': loan_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_loan(request, pk):
    try:
        data = request.data
        try:
            loan = HR_Loans.objects.get(pk=pk)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        loan_serializer = HR_Loans_Serializer(loan, data, partial=True)
        if loan_serializer.is_valid():
            loan_serializer.save()
            return Response(loan_serializer.data, status=status.HTTP_200_OK)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_loan(request, pk):
    try:
        try:
            loan = HR_Loans.objects.get(pk=pk)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        loan.delete()
        return Response({'success': 'loan delete successfully!'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

