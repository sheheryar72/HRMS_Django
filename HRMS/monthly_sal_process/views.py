from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HR_Emp_Monthly_Sal_Mstr, HR_Emp_Monthly_Sal_Dtl
from .serializer import HR_Emp_Monthly_Sal_Dtl_Serializer, HR_Emp_Monthly_Sal_Mstr_Serializer
from employee.models import HR_Employees
from employee.serializers import HR_Employees_Serializer
from django.db.models import Subquery
from rest_framework import status
from payroll_element.models import HR_Payroll_Elements, HR_Payroll_Elements_Serializer
import pdb
from payroll_period.models import *
from salary_update.models import HR_Emp_Sal_Update_Mstr, HR_Emp_Sal_Update_Dtl
from salary_update.serializer import *
from django.db.models import Max
from django.db import models, transaction
from django.db.models import F, Value, FloatField
from django.db.models.functions import Cast
from django.utils import timezone
from django.db import connection
from django.http import JsonResponse
from grade.models import HR_Grade
from designation.models import HR_Designation
from department.models import HR_Department
from django.db.models import Sum, F, Value
from django.db import transaction
from django.db.models import Sum, F, Value, Case, When
from django.db.models.functions import Coalesce
from django.db import transaction


def salaryprocess_view(request):
    return render(request, 'salaryprocess.html')

def monthlysalaryupdate_view(request):
    return render(request, 'monthlysalaryupdate.html')


# def hr_monthly_salary_process(payroll_id, fuel_rate):
#     # Fetch the payroll period start and end dates
#     print('hr_monthly_salary_process called! ')
#     print('hr_monthly_salary_process payroll_id! ', payroll_id)
#     print('hr_monthly_salary_process fuel_rate! ', fuel_rate)
#     try:
#         payroll_period = HR_PAYROLL_PERIOD.objects.get(PAYROLL_ID=payroll_id)
#         sdt = payroll_period.sdt
#         edt = payroll_period.edt
#     except HR_PAYROLL_PERIOD.DoesNotExist:
#         raise ValueError("Payroll period not found.")
    
#     # Check if there is data to process
#     if not HR_Emp_Sal_Update_Mstr.objects.filter(
#         Emp_ID__Emp_Status=1,
#         stop_salary=False
#     ).exists():
#         raise ValueError("No data available for processing.")

#     with transaction.atomic():
#         # Process each employee
#         for emp in HR_Emp_Sal_Update_Mstr.objects.filter(
#             Emp_ID__Emp_Status=1,
#             stop_salary=False
#         ).values('emp_up_id', 'emp_id', 'hr_emp_id').distinct():
            
#             emp_up_id = emp['Emp_Up_ID']
#             emp_id = emp['Emp_ID']
#             hr_emp_id = emp['HR_Emp_ID']
            
#             # Create record in Monthly Salary Master
#             HR_Emp_Monthly_Sal_Mstr.objects.create(
#                 Emp_Up_Date=sdt,
#                 Emp_Category=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Emp_Category,
#                 Marital_Status=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Marital_Status,
#                 No_of_Children=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).No_of_Children,
#                 Co_ID=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Co_ID,
#                 GrossSalary=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).GrossSalary,
#                 Remarks=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Remarks,
#                 Emp_ID=HR_Employees.objects.get(Emp_ID=emp_id),
#                 HR_Emp_ID=hr_emp_id,
#                 Grade_ID=HR_Grade.objects.get(Grade_ID=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Grade_ID),
#                 Dsg_ID=HR_Designation.objects.get(DSG_ID=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Dsg_ID),
#                 Dept_ID=HR_Department.objects.get(Dept_ID=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Dept_ID),
#                 Transfer_Type=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Transfer_Type,
#                 Account_No=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Account_No,
#                 Bank_Name=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Bank_Name,
#                 Stop_Salary=HR_Emp_Sal_Update_Mstr.objects.get(emp_id=emp_id).Stop_Salary,
#                 Payroll_ID=HR_PAYROLL_PERIOD.objects.get(PAYROLL_ID=payroll_id)
#             )
            
#             # Create records in Monthly Salary Detail
#             salary_details = HR_Emp_Sal_Update_Dtl.objects.filter(emp_id=emp_id)
#             for detail in salary_details:
#                 HR_Emp_Monthly_Sal_Dtl.objects.create(
#                     Emp_Up_ID=HR_Emp_Monthly_Sal_Mstr.objects.get(Emp_Up_ID=emp_up_id),
#                     Amount=detail.Amount,
#                     Element_ID=HR_Payroll_Elements.objects.get(Element_ID=detail.Element_ID),
#                     Element_Type=detail.Element_Type,
#                     Element_Category=detail.Element_Category,
#                     Emp_ID=HR_Employees.objects.get(Emp_ID=emp_id)
#                 )
        
#         # Update Additional Elements if needed
#         additional_elements = HR_Payroll_Elements.objects.filter(element_category='Additional')
#         if additional_elements.exists():
#             for element in additional_elements:
#                 if element.Cal_Type == 'Fixed':
#                     HR_Emp_Monthly_Sal_Dtl.objects.filter(
#                         Emp_ID__in=HR_Emp_Sal_Update_Mstr.objects.filter(emp_id=emp_id),
#                         Element_ID=element
#                     ).update(
#                         # Amount=Coalesce(F('Amount'), Value(0))
#                         Amount=Case(
#                             When(Amount__isnull=True, then=Value(0)),
#                             default=F('Amount')
#                         )
#                     )
#                 elif element.Cal_Type == 'Variable':
#                     HR_Emp_Monthly_Sal_Dtl.objects.filter(
#                         Emp_ID__in=HR_Emp_Sal_Update_Mstr.objects.filter(emp_id=emp_id),
#                         Element_ID=element
#                     ).update(
#                         Amount=F('Amount') * fuel_rate
#                     )

#         # Update Monthly Salary Master with total salary details
#         HR_Emp_Monthly_Sal_Mstr.objects.filter(
#             Payroll_ID=payroll_id
#         ).update(
#               GrossSalary=Sum(
#                 Case(
#                     When(hremp_monthly_sal_dtl_test__Amount__isnull=True, then=Value(0)),
#                     default=F('hremp_monthly_sal_dtl_test__Amount')
#                 )
#             )
#             # GrossSalary=Coalesce(Sum('hremp_monthly_sal_dtl_test__Amount'), Value(0))
#         )

from django.http import HttpResponse




def hr_monthly_salary_process(request, payroll_id, fuel_rate):
    try:
        payroll_period = HR_PAYROLL_PERIOD.objects.get(PAYROLL_ID=payroll_id)
    except HR_PAYROLL_PERIOD.DoesNotExist:
        return HttpResponse("Payroll period does not exist", status=404)

    # Delete existing data in destination tables
    HR_Emp_Monthly_Sal_Mstr.objects.filter(Payroll_ID=payroll_period).delete()
    HR_Emp_Monthly_Sal_Dtl.objects.filter(Payroll_ID=payroll_period).delete()

    # Fetch data for bulk create
    salary_updates = HR_Emp_Sal_Update_Mstr.objects.filter(Stop_Salary=0).select_related('Emp_ID', 'Dsg_ID', 'Dept_ID', 'Grade_ID')
    salary_details = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_ID__in=salary_updates.values('Emp_ID')).select_related('Emp_Up_ID', 'Element_ID', 'Emp_ID')

    # Insert into HR_Emp_Monthly_Sal_Mstr
    salary_masters = [
        HR_Emp_Monthly_Sal_Mstr(
            Payroll_ID=payroll_period,
            Emp_Up_ID=obj.Emp_Up_ID,
            Emp_Up_Date=obj.Emp_Up_Date,
            Emp_ID=obj.Emp_ID,
            Emp_Category=obj.Emp_Category,
            HR_Emp_ID=obj.HR_Emp_ID,
            Marital_Status=obj.Marital_Status,
            No_of_Children=obj.No_of_Children,
            Dsg_ID=obj.Dsg_ID,
            Dept_ID=obj.Dept_ID,
            Grade_ID=obj.Grade_ID,
            Co_ID=obj.Co_ID,
            Remarks=obj.Remarks,
            GrossSalary=obj.GrossSalary,
            MDays=30,
            WDAYS=0,
            ADAYS=0,
            JLDAYS=0,
            Transfer_Type=obj.Transfer_Type,
            Account_No=obj.Account_No,
            Bank_Name=obj.Bank_Name,
            Stop_Salary=obj.Stop_Salary
        )
        for obj in salary_updates
    ]
    HR_Emp_Monthly_Sal_Mstr.objects.bulk_create(salary_masters)

    # Insert into HR_Emp_Monthly_Sal_Dtl
    salary_details_bulk = [
        HR_Emp_Monthly_Sal_Dtl(
            Payroll_ID=payroll_period,
            Emp_Up_ID=obj.Emp_Up_ID.Emp_Up_ID,
            Emp_ID=obj.Emp_ID,
            Element_ID=obj.Element_ID,
            Amount=obj.Amount,
            Element_Type=obj.Element_Type,
            Element_Category=obj.Element_Category
        )
        for obj in salary_details
    ]
    HR_Emp_Monthly_Sal_Dtl.objects.bulk_create(salary_details_bulk)

    # Update Fixed Additional Elements
    for detail in HR_Emp_Monthly_Sal_Dtl.objects.filter(Element_Category='Fixed Additional'):
        emp = HR_Employees.objects.get(Emp_ID=detail.Emp_ID.Emp_ID)
        joining_date = emp.Joining_Date
        last_working_date = emp.Last_Working_Date

        if joining_date and last_working_date:
            total_days = (last_working_date - joining_date).days
            if total_days > 0:
                working_days = (30 - (joining_date - payroll_period.Payroll_Start_Date).days) # Assuming `Payroll_Start_Date` is the start date of the payroll period
                new_amount = (detail.Amount / total_days) * working_days
            else:
                new_amount = 0

            detail.Amount = new_amount
            detail.save()

    return JsonResponse({'results': "Procedure executed successfully!"})



# @api_view(['GET'])
# def transfer_data_to_salary_process(request, payroll_id, fuel_rate):
#     print('transfer_data_to_salary_process called payroll_id: ', payroll_id)
#     try:
#         with connection.cursor() as cursor:

#             query = f'''



# DECLARE @Payroll_ID As Int
# 	SET @Payroll_ID = 12

# 	DECLARE @Fuel_Rate As Int
# 	SET @Fuel_Rate = 270

# 	DECLARE @Emp_UP_ID_Cursor_1 cursor
# 	DECLARE @Emp_ID_Cursor_2 cursor

# 	DECLARE @Emp_ID_Additional_Cursor_3 CURSOR
# 	DECLARE @DATA_EXIST AS INT

# 	DECLARE @CHK_FIXED_ADDITIONAL AS Int

# 	DECLARE @CHK_ADDITIONAL AS Int
	

# 	DECLARE @Emp_UP_ID AS INT
# 	DECLARE @Emp_ID AS INT
# 	DECLARE @CNT AS INT
# 	DECLARE @HR_EMP_ID AS INT

# 	DECLARE @SDT AS DATE
# 	DECLARE @EDT AS DATE

# 	SET @DATA_EXIST = (SELECT COUNT(HR_EMP_ID) AS CNT FROM (
# 							SELECT Max(HESUM.Emp_Up_ID) As [Emp_UP_ID], HESUM.Emp_ID, HESUM.HR_EMP_ID
# 							  FROM HR_Emp_Sal_Update_Mstr HESUM, HR_EMPLOYEES HE
# 							  WHERE 1 = 1
# 							  AND HESUM.EMP_ID = HE.EMP_ID
# 							  AND HE.Emp_Status  = 1
# 							  AND (HESUM.STOP_SALARY IS NULL OR HESUM.Stop_Salary  = 0)
# 							  GROUP BY HESUM.EMP_ID, HESUM.HR_EMP_ID) AS ABC
# 						)	

# 	IF (@DATA_EXIST > 0)
# 		BEGIN
# 			SET @Emp_UP_ID_Cursor_1 = CURSOR FOR 
# 										SELECT Max(HESUM.Emp_Up_ID) As [Emp_UP_ID], HESUM.Emp_ID, HESUM.HR_EMP_ID
# 										FROM HR_Emp_Sal_Update_Mstr HESUM, HR_EMPLOYEES HE
# 										WHERE 1 = 1
# 										AND HESUM.EMP_ID = HE.EMP_ID
# 										AND HE.Emp_Status  = 1
# 										AND (HESUM.STOP_SALARY IS NULL OR HESUM.Stop_Salary  = 0)
# 										GROUP BY HESUM.EMP_ID, HESUM.HR_EMP_ID

# 			OPEN @Emp_UP_ID_Cursor_1
# 			FETCH NEXT FROM @Emp_UP_ID_Cursor_1 INTO @Emp_UP_ID, @Emp_ID, @HR_EMP_ID
# 			WHILE @@FETCH_STATUS = 0
# 			BEGIN	

# 				SET @EDT = (SELECT EDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)

# 				--Month Salary Master File
# 				--========================

# 				INSERT INTO [HR_Emp_Monthly_Sal_Mstr_Test] (
# 				[Payroll_ID], [Emp_Up_ID] ,[Emp_Up_Date] ,[Emp_ID] ,[Emp_Category] ,[HR_Emp_ID] ,[Marital_Status] 
# 				,[No_of_Children] ,[Dsg_ID] ,[Dept_ID] ,[Grade_ID] ,[Co_ID] ,[Remarks] ,[GrossSalary]
# 				,[MDays], [WDAYS], [ADAYS], [JLDAYS], [Transfer_Type] ,[Account_No] ,[Bank_Name] ,[Stop_Salary]
# 				)	
# 				Select @Payroll_ID, Emp_Up_ID ,Emp_Up_Date ,Emp_ID ,Emp_Category ,HR_Emp_ID ,Marital_Status
# 				,No_of_Children ,Dsg_ID ,Dept_ID ,Grade_ID ,Co_ID ,Remarks ,GrossSalary
# 				,Day(@EDT), 0, 0, 0, Transfer_Type ,Account_No ,Bank_Name ,Stop_Salary
# 				FROM HR_Emp_Sal_Update_Mstr
# 				WHERE EMP_ID = @EMP_ID

# 				--Month Salary Detail File
# 				--========================

# 				INSERT INTO [HR_Emp_Monthly_Sal_Dtl_Test] (
# 				[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], [Element_Category]
# 				)	
# 				Select @Payroll_ID, Emp_Up_ID, Emp_ID, Element_ID, Amount, Element_Type, Element_Category
# 				FROM HR_Emp_Sal_Update_Dtl
# 				WHERE 1 = 1 
# 				AND EMP_ID = @EMP_ID

# 				FETCH NEXT FROM @Emp_UP_ID_Cursor_1 INTO @Emp_UP_ID, @Emp_ID, @HR_EMP_ID
# 			END
# 			CLOSE @Emp_UP_ID_Cursor_1
# 			DEALLOCATE @Emp_UP_ID_Cursor_1
# 		END

# 	--Working For Fixed Additional

# 	SET @CHK_FIXED_ADDITIONAL = (SELECT COUNT(*) AS FA_CNT FROM HR_Emp_Monthly_Sal_Dtl_Test
# 	WHERE Element_Category = 'Fixed Additional')

# 	IF (@CHK_FIXED_ADDITIONAL > 0)
# 		BEGIN
# 			DECLARE @Emp_UP_ID_C2 AS INT
# 			DECLARE @EMP_ID_C2 AS INT
# 			DECLARE @Element_ID AS INT
# 			DECLARE @Allowance_Amount AS FLOAT
# 			DECLARE @Element_Type AS VARCHAR(50)
# 			DECLARE @Element_Category AS VARCHAR(50)

# 			SET @SDT = (SELECT SDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)
# 			SET @EDT = (SELECT EDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)

# 			DECLARE @GET_JOINING_DATE AS DATE
# 			DECLARE @GET_Last_Working_Date AS DATE

# 			DECLARE @Allowance_Amount_NEW AS FLOAT
# 			DECLARE @JOINING_DAY_MONTH AS INT
# 			DECLARE @Start_DAY_MONTH AS INT
# 			DECLARE @END_DAY_MONTH AS INT
# 			DECLARE @LAST_DAY_MONTH  AS INT
# 			DECLARE @CALC_DAYS AS INT

# 			SET @Emp_ID_Cursor_2 = CURSOR FOR 
# 										SELECT Emp_UP_ID, EMP_ID, Element_ID, Amount, Element_Type, Element_Category	
# 										From HR_Emp_Monthly_Sal_Dtl_Test
# 										Where 1 = 1 
# 										AND Payroll_ID = 12 --@Payroll_ID 
# 										AND Element_Category = 'Fixed Additional'
# 										ORDER BY EMP_ID, Element_ID
				
# 			OPEN @Emp_ID_Cursor_2
# 			FETCH NEXT FROM @Emp_ID_Cursor_2 INTO @Emp_UP_ID_C2, @EMP_ID_C2, @Element_ID, @Allowance_Amount, @Element_Type, @Element_Category
# 			WHILE @@FETCH_STATUS = 0
# 				BEGIN	

# 					SET @GET_JOINING_DATE = (SELECT JOINING_DATE FROM HR_EMPLOYEES WHERE EMP_ID = @EMP_ID_C2
# 											AND JOINING_DATE BETWEEN @SDT AND @EDT)

# 					IF (LEN(@GET_JOINING_DATE) > 0)
# 						BEGIN

# 							SET @JOINING_DAY_MONTH = (SELECT DAY(@GET_JOINING_DATE))
# 							SET @LAST_DAY_MONTH = (SELECT DAY(@EDT))
# 							SET @CALC_DAYS = (@LAST_DAY_MONTH - @JOINING_DAY_MONTH)

# 							SET @Allowance_Amount_NEW = ((@Allowance_Amount/@LAST_DAY_MONTH) * @CALC_DAYS)

# 							UPDATE HR_Emp_Monthly_Sal_Dtl_Test SET AMOUNT = ROUND(@Allowance_Amount_NEW,0)
# 							WHERE PAYROLL_ID = @PAYROLL_ID
# 							AND EMP_UP_ID = @Emp_UP_ID_C2
# 							AND EMP_ID = @EMP_ID_C2
# 							AND ELEMENT_ID = @Element_ID
# 						END

# 					SET @GET_Last_Working_Date = (SELECT Last_Working_Date FROM HR_EMPLOYEES WHERE EMP_ID = @EMP_ID_C2
# 											AND Last_Working_Date BETWEEN @SDT AND @EDT)

# 					IF (LEN(@GET_Last_Working_Date) > 0)
# 						BEGIN

# 							SET @Start_DAY_MONTH = (SELECT DAY(@SDT))
# 							SET @LAST_DAY_MONTH = (SELECT DAY(@GET_Last_Working_Date))
# 							SET @END_DAY_MONTH = (SELECT DAY(@EDT))
# 							SET @CALC_DAYS = ((@LAST_DAY_MONTH + 1) - @Start_DAY_MONTH)

# 							SET @Allowance_Amount_NEW = ((@Allowance_Amount/@END_DAY_MONTH) * @CALC_DAYS)

# 							--select @EMP_ID_C2, @GET_Last_Working_Date, @Start_DAY_MONTH, @END_DAY_MONTH, @LAST_DAY_MONTH, @CALC_DAYS, @Allowance_Amount_NEW

# 							UPDATE HR_Emp_Monthly_Sal_Dtl_Test SET AMOUNT = ROUND(@Allowance_Amount_NEW,0)
# 							WHERE PAYROLL_ID = @PAYROLL_ID
# 							AND EMP_UP_ID = @Emp_UP_ID_C2
# 							AND EMP_ID = @EMP_ID_C2
# 							AND ELEMENT_ID = @Element_ID
# 						END

# 					FETCH NEXT FROM @Emp_ID_Cursor_2 INTO @Emp_UP_ID_C2, @EMP_ID_C2, @Element_ID, @Allowance_Amount, @Element_Type, @Element_Category
# 				END

# 			CLOSE @Emp_ID_Cursor_2
# 			DEALLOCATE @Emp_ID_Cursor_2
# 		END
	
# 	--Working For Additional

# 	SET @CHK_ADDITIONAL = (SELECT COUNT(*) AS A_CNT FROM HR_Payroll_Elements 
# 							WHERE Element_Category = 'Additional')
# 	--SELECT @CHK_ADDITIONAL
# 	IF (@CHK_ADDITIONAL > 0)
# 		BEGIN
# 			DECLARE @Element_ID_C3 AS INT
# 			DECLARE @Element_Type_C3 AS Varchar(50)
# 			DECLARE @Element_Category_C3 AS Varchar(50)
# 			DECLARE @CAL_TYPE AS VARCHAR(50)

# 			DECLARE @ELEMENT_NAME_ID AS VARCHAR(50)

# 			DECLARE @SDT_C3 AS DATE
# 			DECLARE @EDT_C3 AS DATE


# 			SET @SDT_C3 = (SELECT SDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)
# 			SET @EDT_C3 = (SELECT EDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)

# 			--DECLARE @GET_JOINING_DATE AS DATE
# 				--SELECT * FROM HR_PAYROLL_ELEMENTS WHERE Element_Category = 'Additional'
# 			SET @Emp_ID_Additional_Cursor_3 = CURSOR FOR 
# 										SELECT ELEMENT_ID, CONCAT(REPLACE(Element_Name, ' ', '_'),'_',ELEMENT_ID) AS ELEMENT_NAME_ID, 
# 										ELEMENT_TYPE, ELEMENT_CATEGORY, CAL_TYPE	
# 										From HR_PAYROLL_ELEMENTS
# 										Where 1 = 1 
# 										AND Element_Category = 'Additional'
# 										--AND CAL_TYPE = 'Fixed'
# 										ORDER BY Element_ID
				
# 			OPEN @Emp_ID_Additional_Cursor_3
# 			FETCH NEXT FROM @Emp_ID_Additional_Cursor_3 INTO @Element_ID_C3, @ELEMENT_NAME_ID, @Element_Type_C3, 
# 															@Element_Category_C3, @CAL_TYPE
# 			WHILE @@FETCH_STATUS = 0
# 				BEGIN	
# 					DECLARE @sql NVARCHAR(MAX)
# 					IF (@CAL_TYPE = 'Fixed')
# 						BEGIN
# 							SET @sql = N'
# 										INSERT INTO HR_Emp_Monthly_Sal_Dtl_Test (
# 										[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], 
# 										[Element_Category]
# 										)	
# 										SELECT HMAD.Payroll_ID, HEMSM.EMP_UP_ID, HMAD.Emp_ID,  ' + CAST(@Element_ID_C3 AS NVARCHAR) + ' AS ' + QUOTENAME(CAST(@Element_ID_C3 AS NVARCHAR)) + ', ' + (@ELEMENT_NAME_ID) + ' AS ' + @ELEMENT_NAME_ID + ', '''+
# 										(@Element_Type_C3)  + ''' AS ' + @Element_Type_C3 + ', '''	+	(@Element_Category_C3)  + ''' AS ' + @Element_Category_C3 + '
# 										FROM HR_Monthly_All_Ded HMAD
# 										JOIN HR_Emp_Monthly_Sal_Mstr_TEST HEMSM
# 										ON HMAD.EMP_ID = HEMSM.EMP_ID
# 										WHERE HMAD.Payroll_ID = ' + Cast(@Payroll_ID As NVARCHAR) + '
# 										AND ' + QUOTENAME(@ELEMENT_NAME_ID) + ' > 0'										
# 										EXEC sp_executesql @sql
# 						END



# 					IF (@CAL_TYPE = 'Calculate')
# 						BEGIN
# 							SET @LAST_DAY_MONTH = (SELECT DAY(@EDT))

# 							IF (@Element_ID_C3 = 4)  
# 								BEGIN
# 								SET @sql = N'	
# 										INSERT INTO HR_Emp_Monthly_Sal_Dtl_Test (
# 										[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], 
# 										[Element_Category]
# 										)
# 										SELECT HMAD.Payroll_ID, HEMSM.EMP_UP_ID, HMAD.Emp_ID,  ' + CAST(@Element_ID_C3 AS NVARCHAR) + ' AS ' + QUOTENAME(CAST(@Element_ID_C3 AS NVARCHAR)) + ', ' + '
# 										Round((((HEMSM.GrossSalary /' + CAST(@LAST_DAY_MONTH AS NVARCHAR)  + ')/8) * ' +  CAST(@ELEMENT_NAME_ID  AS NVARCHAR) + '),0) AS ' + @ELEMENT_NAME_ID + ', '''+
# 										(@Element_Type_C3)  + ''' AS ' + @Element_Type_C3 + ', '''	+	(@Element_Category_C3)  + ''' AS ' + @Element_Category_C3 + '
# 										FROM HR_Monthly_All_Ded HMAD
# 										JOIN HR_Emp_Monthly_Sal_Mstr_TEST HEMSM
# 										ON HMAD.EMP_ID = HEMSM.EMP_ID
# 										WHERE HMAD.Payroll_ID = ' + CAST(@Payroll_ID AS NVARCHAR) + '
# 										AND ' + QUOTENAME(@ELEMENT_NAME_ID) + ' > 0'	
# 										--select @sql
# 										EXEC sp_executesql @sql
# 								END

# 							IF (@Element_ID_C3 = 22)  
# 								BEGIN
# 									SET @sql = N'	
# 											INSERT INTO HR_Emp_Monthly_Sal_Dtl_Test (
# 											[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], 
# 											[Element_Category]
# 											)
# 											SELECT HMAD.Payroll_ID, HEMSM.EMP_UP_ID, HMAD.Emp_ID,  ' + CAST(@Element_ID_C3 AS NVARCHAR) + ' AS ' + QUOTENAME(CAST(@Element_ID_C3 AS NVARCHAR)) + ', ' + '
# 											Round((' + CAST(@Fuel_Rate  AS NVARCHAR) + ' * ' +  CAST(@ELEMENT_NAME_ID  AS NVARCHAR) + '),0) AS ' + @ELEMENT_NAME_ID + ', '''+
# 											(@Element_Type_C3)  + ''' AS ' + @Element_Type_C3 + ', '''	+	(@Element_Category_C3)  + ''' AS ' + @Element_Category_C3 + '
# 											FROM HR_Monthly_All_Ded HMAD
# 											JOIN HR_Emp_Monthly_Sal_Mstr_TEST HEMSM
# 											ON HMAD.EMP_ID = HEMSM.EMP_ID
# 											WHERE HMAD.Payroll_ID = ' + CAST(@Payroll_ID AS NVARCHAR) + '
# 											AND ' + QUOTENAME(@ELEMENT_NAME_ID) + ' > 0'	
# 											--select @sql
# 											EXEC sp_executesql @sql
# 								END
# 								IF (@Element_ID_C3 = 19)  
# 								BEGIN
# 								SET @sql = N'	
# 										INSERT INTO HR_Emp_Monthly_Sal_Dtl_Test (
# 										[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], 
# 										[Element_Category]
# 										)
# 										SELECT HMAD.Payroll_ID, HEMSM.EMP_UP_ID, HMAD.Emp_ID,  ' + CAST(@Element_ID_C3 AS NVARCHAR) + ' AS ' + QUOTENAME(CAST(@Element_ID_C3 AS NVARCHAR)) + ', ' + '
# 										Round(((HEMSM.GrossSalary /' + CAST(@LAST_DAY_MONTH AS NVARCHAR)  + ') * ' +  CAST(@ELEMENT_NAME_ID  AS NVARCHAR) + '),0) AS ' + @ELEMENT_NAME_ID + ', '''+
# 										(@Element_Type_C3)  + ''' AS ' + @Element_Type_C3 + ', '''	+	(@Element_Category_C3)  + ''' AS ' + @Element_Category_C3 + '
# 										FROM HR_Monthly_All_Ded HMAD
# 										JOIN HR_Emp_Monthly_Sal_Mstr_TEST HEMSM
# 										ON HMAD.EMP_ID = HEMSM.EMP_ID
# 										WHERE HMAD.Payroll_ID = ' + CAST(@Payroll_ID AS NVARCHAR) + '
# 										AND ' + QUOTENAME(@ELEMENT_NAME_ID) + ' > 0'	
# 										--select @sql
# 										EXEC sp_executesql @sql
# 								END
# 						END


# 					FETCH NEXT FROM @Emp_ID_Additional_Cursor_3 INTO @Element_ID_C3, @ELEMENT_NAME_ID, @Element_Type_C3, 
# 															      @Element_Category_C3, @CAL_TYPE

# 					UPDATE HR_Emp_Monthly_Sal_Mstr_Test
# 					SET          HR_Emp_Monthly_Sal_Mstr_Test.ADays = Absent_Days_19
# 					FROM     HR_Emp_Monthly_Sal_Mstr_Test INNER JOIN
# 									  HR_Monthly_All_Ded ON HR_Emp_Monthly_Sal_Mstr_Test.Payroll_ID = HR_Monthly_All_Ded.Payroll_ID 
# 									  AND HR_Emp_Monthly_Sal_Mstr_Test.Emp_ID = HR_Monthly_All_Ded.Emp_ID
# 				END

# 			CLOSE @Emp_ID_Additional_Cursor_3
# 			DEALLOCATE @Emp_ID_Additional_Cursor_3
# 		END


# 	DECLARE @Emp_JOINING_LWD_ABSENT_Cursor_4 AS CURSOR

# 	DECLARE @Emp_UP_ID_C4 AS INT
# 	DECLARE @Emp_ID_C4 AS INT
# 	DECLARE @HR_EMP_ID_C4 AS INT
# 	DECLARE @TYPE AS VARCHAR(10)
# 	DECLARE @JL_DATE AS DATE

# 	DECLARE @COUNT_EMP_DOJ_LWD AS INT

# 	SET @SDT = (SELECT SDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)
# 	SET @EDT = (SELECT EDT FROM HR_PAYROLL_PERIOD_V WHERE PAYROLL_ID = @PAYROLL_ID)

# 	SET @COUNT_EMP_DOJ_LWD = (SELECT COUNT(*) FROM (	SELECT Max(HESUM.Emp_Up_ID) As [Emp_UP_ID], HESUM.Emp_ID, HESUM.HR_EMP_ID, 
# 													HEDLV.TYPE, HEDLV.JL_DATE
# 													FROM HR_Emp_Sal_Update_Mstr HESUM, HR_EMP_DOJ_LWD_V  HEDLV
# 													WHERE 1 = 1
# 													AND HESUM.EMP_ID = HEDLV.EMP_ID
# 													AND HEDLV.Emp_Status  = 1
# 													AND (HESUM.STOP_SALARY IS NULL OR HESUM.Stop_Salary  = 0)
# 													AND HEDLV.JL_DATE BETWEEN @SDT AND @EDT
# 													AND DAY(HEDLV.JL_DATE) NOT IN(DAY(@SDT), DAY(@EDT))
# 													GROUP BY HESUM.EMP_ID, HESUM.HR_EMP_ID, HEDLV.TYPE, HEDLV.JL_DATE) AS ABC)

# 	IF (@COUNT_EMP_DOJ_LWD > 0)
# 		BEGIN
# 		SET @Emp_JOINING_LWD_ABSENT_Cursor_4 = CURSOR FOR 
# 														SELECT Max(HESUM.Emp_Up_ID) As [Emp_UP_ID], HESUM.Emp_ID, HESUM.HR_EMP_ID, 
# 														HEDLV.TYPE, HEDLV.JL_DATE
# 														FROM HR_Emp_Sal_Update_Mstr HESUM, HR_EMP_DOJ_LWD_V  HEDLV
# 														WHERE 1 = 1
# 														AND HESUM.EMP_ID = HEDLV.EMP_ID
# 														AND HEDLV.Emp_Status  = 1
# 														AND (HESUM.STOP_SALARY IS NULL OR HESUM.Stop_Salary  = 0)
# 														AND HEDLV.JL_DATE BETWEEN @SDT AND @EDT
# 														AND DAY(HEDLV.JL_DATE) NOT IN(DAY(@SDT), DAY(@EDT))
# 														GROUP BY HESUM.EMP_ID, HESUM.HR_EMP_ID, HEDLV.TYPE, HEDLV.JL_DATE
# 														ORDER BY Max(HESUM.Emp_Up_ID), HESUM.EMP_ID

# 			OPEN @Emp_JOINING_LWD_ABSENT_Cursor_4
# 			FETCH NEXT FROM @Emp_JOINING_LWD_ABSENT_Cursor_4 INTO @Emp_UP_ID_C4, @Emp_ID_C4, @HR_EMP_ID_C4, @TYPE, @JL_DATE
# 			WHILE @@FETCH_STATUS = 0
# 			BEGIN	

# 			DECLARE @GROSS_SALARY AS FLOAT
# 			DECLARE @JLDays as int
# 			SET @JLDays = 0
# 			SET @GROSS_SALARY = (SELECT GROSSSALARY FROM HR_Emp_Monthly_Sal_Mstr_Test 
# 								WHERE Emp_UP_ID = @Emp_UP_ID_C4
# 								AND EMP_ID = @Emp_ID_C4
# 								AND PAYROLL_ID = @Payroll_ID)

# 			DECLARE @CHK_ABSENT_MONHLY_DED_AMT AS FLOAT
# 			SET @CHK_ABSENT_MONHLY_DED_AMT = 0
# 			SET @CHK_ABSENT_MONHLY_DED_AMT = (SELECT SUM(AMOUNT) FROM HR_Emp_Monthly_Sal_DTL_Test 
# 												WHERE @Emp_UP_ID = @Emp_UP_ID_C4
# 												AND EMP_ID = @Emp_ID_C4
# 												AND PAYROLL_ID =@Payroll_ID
# 												AND ELEMENT_ID = 19)

# 				IF (LEN(@JL_DATE) > 0 AND @TYPE = 'DOJ')
# 					BEGIN

# 						SET @JOINING_DAY_MONTH = (SELECT DAY(@JL_DATE))
# 						SET @LAST_DAY_MONTH = (SELECT DAY(@EDT))
# 						SET @CALC_DAYS = (@LAST_DAY_MONTH - (@LAST_DAY_MONTH - @JOINING_DAY_MONTH))

# 						SET @Allowance_Amount_NEW = ROUND(((@GROSS_SALARY/@LAST_DAY_MONTH) * @CALC_DAYS),0)

# 						UPDATE HR_Emp_Monthly_Sal_Mstr_Test Set JLDays = @CALC_DAYS + @JLDays
# 						WHERE PAYROLL_ID = @PAYROLL_ID
# 						AND EMP_UP_ID = @Emp_UP_ID_C4
# 						AND EMP_ID = @EMP_ID_C4

# 						IF (@CHK_ABSENT_MONHLY_DED_AMT > 0) 
# 							BEGIN
# 								SET @Allowance_Amount_NEW = @Allowance_Amount_NEW + @CHK_ABSENT_MONHLY_DED_AMT

# 								UPDATE HR_Emp_Monthly_Sal_Dtl_Test SET AMOUNT = ROUND(@Allowance_Amount_NEW,0)
# 								WHERE PAYROLL_ID = @PAYROLL_ID
# 								AND EMP_UP_ID = @Emp_UP_ID_C4
# 								AND EMP_ID = @EMP_ID_C4
# 								AND ELEMENT_ID = 19
# 							END
# 						ELSE
# 							BEGIN
# 								INSERT INTO [HR_Emp_Monthly_Sal_Dtl_Test] (
# 								[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], [Element_Category]
# 								) VALUES
# 								(@Payroll_ID, @Emp_UP_ID_C4, @EMP_ID_C4, 19, @Allowance_Amount_NEW, 'Deduction', 'Additional')
# 							END						

# 					END


# 					IF (LEN(@JL_DATE) > 0 AND @TYPE = 'LWD')
# 						BEGIN

# 							SET @JOINING_DAY_MONTH = (SELECT DAY(@JL_DATE))
# 							SET @LAST_DAY_MONTH = (SELECT DAY(@EDT))
# 							SET @END_DAY_MONTH = (SELECT DAY(@JL_DATE))

# 							SET @CALC_DAYS = ((@LAST_DAY_MONTH - @END_DAY_MONTH))

# 							UPDATE HR_Emp_Monthly_Sal_Mstr_Test Set JLDays = @CALC_DAYS
# 							WHERE PAYROLL_ID = @PAYROLL_ID
# 							AND EMP_UP_ID = @Emp_UP_ID_C4
# 							AND EMP_ID = @EMP_ID_C4

# 							SET @Allowance_Amount_NEW = ROUND(((@GROSS_SALARY/@LAST_DAY_MONTH) * @CALC_DAYS),0)

# 						IF (@CHK_ABSENT_MONHLY_DED_AMT > 0) 
# 							BEGIN
# 								SET @Allowance_Amount_NEW = @Allowance_Amount_NEW + @CHK_ABSENT_MONHLY_DED_AMT

# 								UPDATE HR_Emp_Monthly_Sal_Dtl_Test SET AMOUNT = ROUND(@Allowance_Amount_NEW,0)
# 								WHERE PAYROLL_ID = @PAYROLL_ID
# 								AND EMP_UP_ID = @Emp_UP_ID_C4
# 								AND EMP_ID = @EMP_ID_C4
# 								AND ELEMENT_ID = 19
# 							END
# 						ELSE
# 							BEGIN
# 								INSERT INTO [HR_Emp_Monthly_Sal_Dtl_Test] (
# 								[Payroll_ID], [Emp_Up_ID], [Emp_ID], [Element_ID], [Amount], [Element_Type], [Element_Category]
# 								) VALUES
# 								(@Payroll_ID, @Emp_UP_ID_C4, @EMP_ID_C4, 19, @Allowance_Amount_NEW, 'Deduction', 'Additional')
# 							END

# 						END

# 			FETCH NEXT FROM @Emp_JOINING_LWD_ABSENT_Cursor_4 INTO @Emp_UP_ID_C4, @Emp_ID_C4, @HR_EMP_ID_C4, @TYPE, @JL_DATE
# 			END
# 		CLOSE @Emp_JOINING_LWD_ABSENT_Cursor_4
# 		DEALLOCATE @Emp_JOINING_LWD_ABSENT_Cursor_4
# 	END

# 	UPDATE HR_Emp_Monthly_Sal_Mstr_Test Set WDays = (MDAYS - (ADAYS + JLDays))
# 	WHERE PAYROLL_ID = @PAYROLL_ID

# '''

#             cursor.execute(query)
#             return Response({'status': 'Data transferred successfully.'})

#     except Exception as e:
#         return Response({'status': 'Error occurred.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
def transfer_data_to_salary_process(request, payroll_id, fuel_rate):
    print('transfer_data_to_salary_process called payroll_id: ', payroll_id)
    try:
        with connection.cursor() as cursor:
            # Execute the stored procedure
            # cursor.execute("EXEC dbo.HR_Monthly_Salary_Process @m_Payroll_ID=%s, @m_Fuel_Rate=%s", [payroll_id, fuel_rate])
            # Fetch the number of rows affected
            
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}")

            # You can also fetch results if needed, for debugging or logging
            # results = cursor.fetchall()

        # Return a success response
        return JsonResponse({'results': f"Procedure executed successfully. Rows affected: {rows_affected}"})
    except Exception as e:
        # Log the error internally (consider using Django logging)
        print(f"Error executing stored procedure: {str(e)}")

        # Return a success response but include the error message
        return JsonResponse({'results': 'Procedure executed with errors', 'error': str(e)}, status=500)


# @api_view(['GET'])
# def transfer_data_to_salary_process(request, payroll_id, fuel_rate):
#     print('transfer_data_to_salary_process called payroll_id: ', payroll_id)
#     try:
#         with connection.cursor() as cursor:
#             # fuel_rate = 280
#             # Call the stored procedure
#             cursor.execute("EXEC dbo.HR_Monthly_Salary_Process2 @m_Payroll_ID=%s, @m_Fuel_Rate=%s", [payroll_id, fuel_rate])
#             # Fetch the results if the stored procedure returns any
#             # results = cursor.fetchall()

#             rows_affected = cursor.rowcount
#             print(f"Rows affected: {rows_affected}")
        
#         # Return the results as JSON
#         return JsonResponse({'results': "results"})
#     except Exception as e:
#         # Handle any exceptions that may occur
#         return JsonResponse({'error': str(e)}, status=500)


# @api_view(['GET'])
# def getall_monthly_salary_mstr(request):
#     try:
#         queryset = HR_Emp_Monthly_Sal_Mstr.objects.all()
#         serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(queryset, many=True)
#         return Response(serializer.data, status=200)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# @api_view(['POST'])
# def transfer_data_to_salary_process(request, period_id):
#     print('transfer_data_to_salary_process called!')
#     try:
#         max_emp_mst_up_ids = HR_Emp_Sal_Update_Mstr.objects.values('Emp_ID').annotate(max_emp_mst_up_id=Max('Emp_Up_ID'))
#         max_emp_mst_up_id_values = [item['max_emp_mst_up_id'] for item in max_emp_mst_up_ids]

#         print('max_emp_mst_up_id_values: ', max_emp_mst_up_id_values)

#         max_emp_mst_records = HR_Emp_Sal_Update_Mstr.objects.filter(Emp_Up_ID__in=max_emp_mst_up_id_values)
#         max_emp_dtl_records = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID__in=max_emp_mst_up_id_values)

#         # print('max_emp_mst_records: ', max_emp_mst_records)
#         # print('max_emp_dtl_records: ', max_emp_dtl_records)

#         # Update Period_ID for mst records
#         for record in max_emp_mst_records:
#             record.Period_ID = period_id
#             record.save()

#         # Serialize and save the mst and dtl records
#         mst_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=max_emp_mst_records, many=True)
#         if mst_serializer.is_valid():
#             print('mst_serializer.data: ', mst_serializer.data)
#             mst_serializer.save()
#         else:
#             return Response(mst_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         dtl_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=max_emp_dtl_records, many=True)
#         if dtl_serializer.is_valid():
#             print('dtl_serializer.data: ', dtl_serializer.data)
#             dtl_serializer.save()
#         else:
#             return Response(dtl_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(data=mst_serializer.data, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# def hr_monthly_salary_process(payroll_id: int, fuel_rate: float):
#     with transaction.atomic():
#         # Get the start and end dates for the payroll period
#         payroll_period = HRPayPeriod.objects.get(payroll_id=payroll_id)
#         sdt, edt = payroll_period.sdt, payroll_period.edt

#         # Check for data existence
#         data_exists = HREmpSalUpdateMstr.objects.filter(
#             emp_id__emp_status=True,
#             stop_salary__isnull=True
#         ).exists()

#         if data_exists:
#             # Insert into HR_Emp_Monthly_Sal_Mstr_Test
#             sal_update_mstrs = HREmpSalUpdateMstr.objects.filter(
#                 emp_id__emp_status=True,
#                 stop_salary__isnull=True
#             )

#             for sal_update in sal_update_mstrs:
#                 HREmpMonthlySalMstrTest.objects.create(
#                     payroll_id=payroll_id,
#                     emp_up_id=sal_update.emp_up_id,
#                     emp_up_date=sal_update.emp_up_date,
#                     emp_id=sal_update.emp_id,
#                     hr_emp_id=sal_update.hr_emp_id,
#                     # Set other fields as needed
#                 )

#             # Insert into HR_Emp_Monthly_Sal_Dtl_Test
#             sal_update_dtls = sal_update_mstrs.values('emp_id').distinct()
#             for sal_update_dtl in sal_update_dtls:
#                 details = HREmpSalUpdateDtl.objects.filter(emp_id=sal_update_dtl['emp_id'])
#                 for detail in details:
#                     HREmpMonthlySalDtlTest.objects.create(
#                         payroll_id=payroll_id,
#                         emp_up_id=sal_update.emp_up_id,
#                         emp_id=sal_update.emp_id,
#                         element_id=detail.element_id,
#                         amount=detail.amount,
#                         # Set other fields as needed
#                     )

#             # Process Fixed Additional
#             fixed_additionals = HREmpMonthlySalDtlTest.objects.filter(
#                 element_category='Fixed Additional'
#             )

#             for additional in fixed_additionals:
#                 joining_date = HREmployee.objects.get(emp_id=additional.emp_id).joining_date
#                 if joining_date:
#                     joining_day_month = joining_date.day
#                     last_day_month = edt.day
#                     calc_days = last_day_month - joining_day_month

#                     allowance_amount_new = (additional.amount / last_day_month) * calc_days
#                     additional.amount = round(allowance_amount_new, 0)
#                     additional.save()

#                 last_working_date = HREmployee.objects.get(emp_id=additional.emp_id).last_working_date
#                 if last_working_date:
#                     start_day_month = sdt.day
#                     end_day_month = last_working_date.day
#                     calc_days = (end_day_month + 1) - start_day_month

#                     allowance_amount_new = (additional.amount / end_day_month) * calc_days
#                     additional.amount = round(allowance_amount_new, 0)
#                     additional.save()

#             # Process Additional
#             additional_elements = HRPayrollElements.objects.filter(element_category='Additional')

#             for element in additional_elements:
#                 if element.cal_type == 'Fixed':
#                     # Handle Fixed Calculation
#                     pass
#                 elif element.cal_type == 'Calculate':
#                     # Handle Calculate
#                     if element.element_id == 4:
#                         # Your calculation logic
#                         pass
#                     elif element.element_id == 22:
#                         HREmpMonthlySalDtlTest.objects.filter(
#                             element_id=element.element_id,
#                             amount__gt=0
#                         ).update(
#                             amount=Cast(
#                                 Value(fuel_rate) * F('amount'),
#                                 FloatField()
#                             )
#                         )
#                     elif element.element_id == 19:
#                         # Your calculation logic
#                         pass



# @api_view(['POST'])
# def transfer_data_to_salary_process(request, period_id):
#     print('transfer_data_to_salary_process called!')
#     try:
#         # Get the latest update master record IDs for each employee
#         max_emp_mst_up_ids = HR_Emp_Sal_Update_Mstr.objects.values('Emp_ID').annotate(max_emp_mst_up_id=Max('Emp_Up_ID'))

#         max_emp_mst_up_id_values = [item['max_emp_mst_up_id'] for item in max_emp_mst_up_ids]

#         print('max_emp_mst_up_id_values: ', max_emp_mst_up_id_values)

#         # Fetch the master and detail records
#         max_emp_mst_records = HR_Emp_Sal_Update_Mstr.objects.filter(Emp_Up_ID__in=max_emp_mst_up_id_values)
#         max_emp_dtl_records = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID__in=max_emp_mst_up_id_values)

#         # print('max_emp_mst_records: ', max_emp_mst_records)
#         # print('max_emp_dtl_records: ', max_emp_dtl_records)

#         # Prepare data for master records
#         mst_data = []
#         for record in max_emp_mst_records:
#             mst_data.append({
#                 'Emp_Up_ID': record.Emp_Up_ID,
#                 'Emp_Up_Date': record.Emp_Up_Date,
#                 'Emp_Category': record.Emp_Category,
#                 'Marital_Status': record.Marital_Status,
#                 'No_of_Children': record.No_of_Children,
#                 'Co_ID': record.Co_ID,
#                 'GrossSalary': record.GrossSalary,
#                 'Remarks': record.Remarks,
#                 'Emp_ID': record.Emp_ID.Emp_ID,
#                 'HR_Emp_ID': record.HR_Emp_ID,
#                 'Grade_ID': record.Grade_ID.Grade_ID,
#                 'Dsg_ID': record.Dsg_ID.DSG_ID,
#                 'Dept_ID': record.Dept_ID.Dept_ID,
#                 'Transfer_Type': record.Transfer_Type,
#                 'Account_No': record.Account_No,
#                 'Bank_Name': record.Bank_Name,
#                 'Stop_Salary': record.Stop_Salary,
#                 'Period_ID': period_id,
#             })

#         # Serialize and save master records
#         mst_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=mst_data, many=True)


#         if mst_serializer.is_valid():
#             mst_serializer.save()
#             print('mst_serializer.data: ', mst_serializer.data)
#         else:
#             return Response(mst_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Prepare data for detail records
#         dtl_data = []
#         for record in max_emp_dtl_records:
#             dtl_data.append({
#                 'Emp_Up_ID': record.Emp_Up_ID.Emp_Up_ID,
#                 'Amount': record.Amount,
#                 'Element_ID': record.Element_ID.Element_ID,
#                 'Element_Type': record.Element_Type,
#                 'Element_Category': record.Element_Category,
#                 'Emp_ID': record.Emp_ID.Emp_ID,
#             })

#         # Serialize and save detail records
#         dtl_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=dtl_data, many=True)


#         if dtl_serializer.is_valid():
#             print('dtl_serializer.data: ', dtl_serializer.data)
#             dtl_serializer.save()
#         else:
#             return Response(dtl_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(data={"status": "yes"}, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     

    

        
@api_view(['GET'])
def getall_payrollperiod(request):
    try:
        payroll_periods = HR_PAYROLL_PERIOD.objects.select_related('MNTH_ID', 'FYID').all()

        data = []

        for payroll_period in payroll_periods:
            data.append({
                'PAYROLL_ID': payroll_period.PAYROLL_ID,
                'PERIOD_ID': payroll_period.PERIOD_ID,
                'MNTH_NAME': payroll_period.MNTH_ID.MNTH_NAME,
                'FinYear': payroll_period.FYID.FinYear
            })

        return Response(data=data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_active_period(request):
    try:
        payroll_period = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True, FYID__FYID=1).select_related('MNTH_ID', 'FYID').first()

        payroll_period.FYID.FinYear

        data = {
            'PAYROLL_ID': payroll_period.PAYROLL_ID,
            'PERIOD_ID': payroll_period.PERIOD_ID,
            'MNTH_NAME': payroll_period.MNTH_ID.MNTH_NAME,
            'FinYear': payroll_period.FYID.FinYear
        }

        return Response(data=data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])  
def getall_salaryprocess(request):
    try:
        emp_ids = HR_Emp_Monthly_Sal_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryprocess = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()    
        serializer = HR_Employees_Serializer(queryset_emp_salaryprocess, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])  
def getll_emp_notin_salaryprocess(request):
    try:
        emp_ids = HR_Emp_Monthly_Sal_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryprocess = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()
        serializer = HR_Employees_Serializer(queryset_emp_salaryprocess, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_salary_update(request):
        try:
            # print("add_salary_update data: ", request.data)   
            # pdb.set_trace()
            print("add_salary_update")
            print("masterData data: ", request.data.get("masterData", {}))
            print("detailList data: ", request.data.get('detailList', []))
            master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=request.data.get("masterData", {}))
            if master_serializer.is_valid():
                master_serializer.save()
                print("master saved")
                print("master_serializer: ", master_serializer.data)
                print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
                detailList = request.data.get('detailList', [])
                for detail_data in detailList:
                    detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
                    detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
                    detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
                    if detail_serializer.is_valid():
                        detail_serializer.save()
                        print("detail saved")
                    else:
                        return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(master_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def update_salary_update(request, empupid):
#         try:
#             print("update_salary_update")
#             print("empupid: ", empupid)
#             print("masterData data: ", request.data.get("masterData", {}))
#             print("detailList data: ", request.data.get('detailList', []))
#             master_querysery = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=empupid)
#             detail_queryset = HR_Emp_Monthly_Sal_Mstr.objects.get(Emp_Up_ID=empupid)
#             if master_querysery is None:
#                 Response({'error': 'no salary found'}, status=status.HTTP_404_NOT_FOUND)
            
#             # if master_querysery and detail_queryset is not None:
#             #     HR_Emp_Monthly_Sal_Mstr.objects.filter(Emp_Up_ID=empupid).delete()
#             #     HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empupid).delete()

#             master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=request.data.get("masterData", {}))
#             # master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(master_querysery, data=request.data.get("masterData", {}), partial=True)
#             if master_serializer.is_valid():
#                 master_serializer.save()
#                 print("master updated")
#                 print("master_serializer: ", master_serializer.data)
#                 print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
#                 detailList = request.data.get('detailList', [])

#                 for detail_data in detailList:
#                     detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
#                     detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
        
#                     # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.get(Emp_ID=empupid)

#                     detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
#                     if detail_serializer.is_valid():
#                         detail_serializer.save()
#                         print("detail updated")
#                     else:
#                         return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response(master_serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_salary_update(request, empupid):
    try:
        # Fetch master data
        try:
            master_instance = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=empupid)
        except HR_Emp_Monthly_Sal_Mstr.DoesNotExist:
            return Response({'error': 'No salary record found'}, status=status.HTTP_404_NOT_FOUND)

        # Handle master data update
        master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(master_instance, data=request.data.get("masterData", {}), partial=True)
        if master_serializer.is_valid():
            master_instance = master_serializer.save()
            print("Master updated")
            print("Master serializer data:", master_serializer.data)
            print('master_instance.Emp_ID: ', master_instance.Emp_ID)

            detailList = request.data.get('detailList', [])
            for detail_data in detailList:
                detail_data['Emp_Up_ID'] = master_instance.Emp_Up_ID
                detail_data['Emp_ID'] = master_instance.Emp_ID.Emp_ID

                # Handle detail data update
                detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    print("Detail updated")
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(master_serializer.data, status=status.HTTP_200_OK)
        else:
            # Print serializer errors for debugging
            print("Master serializer errors:", master_serializer.errors)
            return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Print exception for debugging
        print("Exception:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# @api_view(['PUT'])
# def update_salary_Update(request, pk):
#     try:
#         master_instance = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=pk)
#         master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(instance=master_instance, data=request.data.get('masterData', {}))
#         if not master_serializer.is_valid():
#             return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         master_serializer.save()

#         detail_querySet_list = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=pk)
#         for detail_querySet in detail_querySet_list:
#             detail_request = next((item for item in request.data.get("detailList", []) if item['id'] == detail_querySet.id), None)
#             if detail_request:
#                 detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(instance=detail_querySet, data=detail_request)
#                 if detail_serializer.is_valid():
#                     detail_serializer.save()
#                 else:
#                     return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message": "Salary update updated successfully"}, status=status.HTTP_200_OK)
#     except HR_Emp_Monthly_Sal_Mstr.DoesNotExist:
#         return Response({'error': 'Master record not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_payroll_element_notin_su(request, empUpID, empID):
    try:
        print('empID: ', empID)
        print('empUpID: ', empUpID)
        if empID is None or empUpID is None:
            return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
        su_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_ID=empID, Emp_Up_ID=empUpID).values_list("Element_ID", flat=True)
        element_queryset = HR_Payroll_Elements.objects.exclude(Element_ID__in=su_queryset)
        serializer = HR_Payroll_Elements_Serializer(element_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_master_byid(request, empUpID, empID):
    try:
        if not empID or not empUpID:
            return Response({'error': 'Employee ID or Update ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        print("up is: ", empUpID)
        print("empID: ", empID)
        # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empUpID)
        detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID).select_related('Emp_Up_ID', 'Emp_ID', 'Element_ID')
        # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID)
        datas = []
        print('detail_queryset: ', detail_queryset)
        for data in detail_queryset:
            print('data: ', data)
            item = {
                "Emp_Up_ID": data.Emp_Up_ID.Emp_Up_ID,
                "Emp_Up_Date": data.Emp_Up_ID.Emp_Up_Date,
                "Emp_ID": data.Emp_ID.Emp_ID,
                "Emp_Name": data.Emp_ID.Emp_Name,
                "HR_Emp_ID": data.Emp_ID.HR_Emp_ID,
                "Emp_Category": data.Emp_Up_ID.Emp_Category,
                "GrossSalary": data.Emp_Up_ID.GrossSalary,  
                "Amount": data.Amount,
                "Element_Category": data.Element_Category,
                "Element_ID": data.Element_ID.Element_ID,
                "Element_Name": data.Element_ID.Element_Name,
                "Element_Type": data.Element_Type,
                "Remarks": data.Emp_Up_ID.Remarks,
                "Grade_ID": data.Emp_Up_ID.Grade_ID.Grade_ID,
                "Grade_Descr": data.Emp_Up_ID.Grade_ID.Grade_Descr,
                "Co_ID": data.Emp_ID.Co_ID,
                "Dsg_ID": data.Emp_Up_ID.Dsg_ID.DSG_ID,
                "DSG_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
                "Dept_ID": data.Emp_Up_ID.Dept_ID.Dept_ID,
                "Dept_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
                "Marital_Status": data.Emp_ID.Marital_Status,
                "No_of_Children": data.Emp_Up_ID.No_of_Children,
                "Transfer_Type": data.Emp_Up_ID.Transfer_Type,
                "Account_No": data.Emp_Up_ID.Account_No,
                "Bank_Name": data.Emp_Up_ID.Bank_Name,
                "Stop_Salary": data.Emp_Up_ID.Stop_Salary,
            }
            datas.append(item)
        # print("DAtas: ", datas)
        return Response(datas, status=status.HTTP_200_OK)
    except HR_Emp_Monthly_Sal_Dtl.DoesNotExist:
        return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getll_master(request):
    try:
        querySet = HR_Emp_Monthly_Sal_Mstr.objects.prefetch_related('Emp_ID', 'Grade_ID', 'Dept_ID')
        print('querySet: ', querySet.count())
        datas = []
        for item in querySet:
            data = {
                'Emp_Up_ID': item.Emp_Up_ID,
                'Emp_Up_Date': item.Emp_Up_Date,
                'Emp_ID': item.Emp_ID.Emp_ID,
                'HR_Emp_ID': item.Emp_ID.HR_Emp_ID,
                'Emp_Name': item.Emp_ID.Emp_Name,
                'Dsg_Descr': item.Dsg_ID.DSG_Descr,
                'Dept_Descr': item.Dept_ID.Dept_Descr
            }
            datas.append(data)
        # print('datas: ', datas)
        return Response(datas, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

