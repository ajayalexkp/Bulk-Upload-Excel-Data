from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import openpyxl
from . models import *
# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel = request.FILES['customer_details']

            if not excel.name.endswith('.xlsx' or 'xls'):
                messages.error(request, 'Please insert Excel File')
                return redirect(upload_file)

            wb = openpyxl.load_workbook(excel)
            ws = wb.active

            details = list()
            for row in ws.iter_rows(min_row=2):
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                if not CustomerDetails.objects.filter(id=row_data[0]).exists():
                    address = CustomerAddress.objects.filter(address=row_data[4]).values('id')
                    obj = CustomerDetails(id=row_data[0], name=row_data[1], gender=row_data[2],
                                          email=row_data[3], address_id=address)
                    details.append(obj)

            CustomerDetails.objects.bulk_create(details)

    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})


def details(request):
    details_list = list(CustomerDetails.objects.all().values('id', 'name', 'gender', 'email', 'address__address'))
    return render(request, 'details.html', {'details_list': details_list})











