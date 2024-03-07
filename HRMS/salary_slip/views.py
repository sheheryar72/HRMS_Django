from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Salary_Slip
from .serializers import Salary_Slip_Serializer
from django.views import View
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.template import Context
# from weasyprint import HTML
from xhtml2pdf import pisa


def salary_slip_view(request):
    print('Salary Slip called')
    return render(request, 'index.html')

@api_view(['GET'])
def get_salary_slip_by_id(request, emp_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC HR_Emp_Salary_Slip_sh @Emp_ID = %s", [emp_id])
            salary_slip_data = cursor.fetchall()
            #print('salary_slip_data: ', salary_slip_data)
            
        if salary_slip_data:
            # Assuming your serializer is properly defined
            serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
            
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
                #return Response({'error': 'Serializer validation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No salary slips found for the given employee'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC HR_Emp_Salary_Slip_sh @Emp_ID = %s", [165])
            salary_slip_data = cursor.fetchall()
            #   print('data: ', salary_slip_data)
        if salary_slip_data:
            # Assuming your serializer is properly defined
            serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
            if serializer.is_valid():
                # Assuming you have context_data to render the template
                context_data = {'data': serializer.data}
                print('serializer: ', serializer.data)
                # Render the Django template to HTML
                html = get_template('salary_slip.html').render(context_data)

                # Create the PDF object using the response object as its "file"
                pisa_status = pisa.CreatePDF(html, dest=response)

                if pisa_status.err:
                    return HttpResponse("Error generating PDF", status=500)

                return response
            else:
                print('serializer: ', serializer.data)
                
                # Assuming you have context_data to render the template
                context_data = {'data': serializer.data}
                #{{data.0.Emp_ID}}


                # Render the Django template to HTML
                html = get_template('salary_slip.html').render(context_data)

                # Create the PDF object using the response object as its "file"
                pisa_status = pisa.CreatePDF(html, dest=response)

                if pisa_status.err:
                    return HttpResponse("Error generating PDF", status=500)

                return response


                #return HttpResponse("Serializer validation failed", status=500)

        return HttpResponse("No salary slips found for the given employee", status=404)

    except Exception as e:
        return HttpResponse(str(e), status=500)



# def generate_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="example.pdf"'

#     with connection.cursor() as cursor:
#         cursor.execute("EXEC HR_Emp_Salary_Slip_sh @Emp_ID = %s", [165])
#         salary_slip_data = cursor.fetchall()
#         print('salary_slip_data: ', salary_slip_data)


#     if salary_slip_data:
#         # Assuming your serializer is properly defined
#         serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
        
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.data, status=status.HTTP_200_OK)


#         # Assuming you have context_data to render the template
#         context_data = {'data': serializer.data}

#         html = get_template('salary_slip.html').render(context_data)

#         # Create the PDF object, using the response object as its "file."
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             return HttpResponse("Error generating PDF", status=500)

#     return response


# def generate_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="example.pdf"'

#     #html = ""
#     html = get_template('salary_slip.html')

#     # Create the PDF object, using the response object as its "file."
#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF", status=500)

#     return response



# def generate_pdf(request):
#     # Get your HTML template
#     template = get_template('salary_slip.html')
    
#     # Prepare context data
#     context = {'data': 'Your data goes here'}

#     # Render the template with context data
#     html_content = template.render(context)

#     # Create a WeasyPrint HTML object
#     html = HTML(string=html_content)

#     # Generate PDF
#     pdf_file = html.write_pdf()

#     # Create HTTP response with PDF content
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="report.pdf"'
#     response.write(pdf_file)

#     return response


# class SalarySlipPDFView(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             # Fetch data from your API using the serializer
#             with connection.cursor() as cursor:
#                 cursor.execute("EXEC HR_Emp_Salary_Slip_sh @Emp_ID = %s", [165])
#                 salary_slip_data = cursor.fetchall()

#             if salary_slip_data:
#                 # Assuming your serializer is properly defined
#                 serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
#                 serializer.is_valid()
#                 salary_slip_data = serializer.validated_data
#             else:
#                 return HttpResponse("No data found. Unable to generate PDF.", status=404)

#             # Create a PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="salary_slip.pdf"'

#             # Create the PDF content using reportlab
#             p = canvas.Canvas(response)
#             # Customize the PDF content based on your data
#             for record in salary_slip_data:
#                 p.drawString(100, 800, f"Employee ID: {record['Emp_ID']}")
#                 p.drawString(100, 780, f"Employee Name: {record['Emp_Name']}")
#                 # Add more fields as needed
#                 p.showPage()

#             p.save()

#             return response

#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}", status=500)



# class SalarySlipPDFView(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             # Fetch data from your API using the serializer
#             # salary_slip_data = get_salary_slip_by_id(request, 165)
#             # serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
#             # print('salary_slip_data: ', salary_slip_data)

#             with connection.cursor() as cursor:
#                 cursor.execute("EXEC HR_Emp_Salary_Slip_sh @Emp_ID = %s", [165])
#                 salary_slip_data = cursor.fetchall()
#                 #print('salary_slip_data: ', salary_slip_data)
            
#             if salary_slip_data:
#                 # Assuming your serializer is properly defined
#                 serializer = Salary_Slip_Serializer(data=salary_slip_data, many=True)
            


#             if serializer.is_valid():
#                 salary_slip_data = serializer.data
#             else:
#                 return HttpResponse("Invalid data. Unable to generate PDF.", status=500)

#             # Create a PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="salary_slip.pdf"'

#             # Create the PDF content using reportlab
#             p = canvas.Canvas(response)
#             # Customize the PDF content based on your data
#             for record in salary_slip_data:
#                 p.drawString(100, 800, f"Employee ID: {record['Emp_ID']}")
#                 p.drawString(100, 780, f"Employee Name: {record['Emp_Name']}")
#                 # Add more fields as needed
#                 p.showPage()

#             p.save()

#             return response

#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}", status=500)
        


