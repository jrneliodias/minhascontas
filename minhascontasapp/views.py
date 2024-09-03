from django.shortcuts import render
from .form import UploadFileForm
import csv
from io import TextIOWrapper
from .models import Register
from django.contrib import messages
from django.utils.dateparse import parse_date
# Create your views here.


def upload_csv(request):
    data = None  # Initialize data variable
    form = UploadFileForm()  # Initialize form outside of if-else to handle both GET and POST

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.reader(csv_file_wrapper)
            data = list(reader)

            # Extract data to display and save to the database
            try:
                saveCSVDatabase(data[1:])  # Pass rows without the header
                messages.success(
                    request, "CSV data uploaded and saved successfully!")
            except Exception as e:
                messages.error(request, f"Error saving data: {e}")
    else:
        form = UploadFileForm()  # Initialize form for a GET request

    return render(request, 'upload.html', {'form': form, 'data': data})


def saveCSVDatabase(data):
    for row in data:
        if len(row) != 5:
            # Skip rows that do not have exactly 4 columns
            continue

        date_str, description, category, payment_form, value_str = row

        # Convert data types as necessary
        try:
            date = parse_date(date_str)  # Converts string to a date object
            value = float(value_str)  # Converts string to a float
        except ValueError as e:
            # Log error or handle it gracefully
            print(f"Error converting row data: {e}")
            continue

        # Save each row to the database
        register = Register(date=date,
                            value=value,
                            description=description,
                            category=category,
                            payment_form=payment_form)
        try:
            register.full_clean()
        except Exception as e:
            # Log error or handle it gracefully
            print(f"Error validating row data: {e}")
            continue
        register.save()
