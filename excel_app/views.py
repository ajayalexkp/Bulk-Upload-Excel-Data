from django.contrib import messages
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd
import openpyxl
import psycopg2
from .models import *


# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel = request.FILES['customer_details']

            if not excel.name.endswith('.xlsx' or 'xls'):
                messages.error(request, 'Please insert Excel File')
                return redirect(upload_file)

            # wb = openpyxl.load_workbook(excel)
            # ws = wb.active

            # df = pd.DataFrame(ws.values)
            df = pd.read_excel(excel)
            print(df)

            # establishing the connection
            conn = psycopg2.connect(
                database="testdb1", user='testuser', password='user@123', host='localhost', port='5432'
            )

            # Setting auto commit false
            # conn.autocommit = True

            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Retrieving data
            query = cursor.execute('SELECT * FROM  excel_app_customeraddress')

            # Fetching 1st row from the table
            # res = cursor.fetchall();
            # print(res)
            obj_list = list(CustomerAddress.objects.values())
            # for obj in obj_list:

            df1 = pd.DataFrame.from_records(obj_list)
            print(df1)
            # Converting list to dataframe
            # df1 = pd.read_sql_query(query)
            # print(df1)

            # Commit your changes in the database
            conn.commit()

            # Closing the connection
            conn.close()

            data = pd.merge(df, df1, on="address")
            print(data)

            df_records = data.to_dict('records')
            record_lst = [CustomerDetails(
                id=record['id_x'],
                name=record['name'],
                gender=record['gender'],
                email=record['email'],
                address_id=record['id_y']
            ) for record in df_records]

            CustomerDetails.objects.bulk_create(record_lst)
            messages.info(request, 'Excel file uploaded successfully.')

    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})


def details_view(request):
    details_list = list(CustomerDetails.objects.all().values('id', 'name', 'gender', 'email', 'address__address'))
    return render(request, 'details.html', {'details_list': details_list})
