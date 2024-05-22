from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from django.contrib.auth.decorators import login_required
from .utils import get_google_credentials
from googleapiclient.discovery import build

from .forms import *


SCOPES = ['https://www.googleapis.com/auth/drive']


# owner onboarding folder - 1ub8g1ll4G0cNYb8OkqbJjwDIrRPHX5-7
# properties folder - 141hQMIqpuAXcwzvAczhiClzFvL-SGemb
# expenses folder - 1LRJmLgbAS339l9Q3IB-iEu0rA-yADlMy

# testing onboarding spreadsheet: 1AxeYumE9OuGkzXluCduJzVSKilLFEz5EIbokH8Q9IQk
# testing onboarding spreadsheet onboarding template gid: 0

# B2 Owner Name
# B3 Start Date
# B4 Launch Date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from googleapiclient.discovery import build
from .utils import get_google_credentials

from .models import OnboardingObject

@login_required
def onboarding_list(request):
    onboarding_objects = OnboardingObject.objects.all()
    return render(request, 'main.html', {'onboarding_objects': onboarding_objects})

# this view will host the dashboard
@login_required
def dashboard(request):
    dashboard_step_one_form = DashboardStepOne()
    return render(request, "dashboard.html", {'dashboard_step_one_form': dashboard_step_one_form})


def dashboard_step_one_view(request):
    if request.method == 'POST':
        form = DashboardStepOne(request.POST)
        if form.is_valid():
            # Process the form data here, e.g., save it to a database or perform other actions
            address = form.cleaned_data['address']
            owner = form.cleaned_data['owner']

            # Assume you save the data here
            creds = get_google_credentials(request.user)

            # Build the Drive v3 API service
            service = build('drive', 'v3', credentials=creds)

            # Parent folder ID - ONBOARDING_AUTOMATION
            parent_folder_id = '16wRNGg-ukWU7X4oW0HoxRfYjLd9DMrbW'

            # Define the folder metadata
            folder_metadata = {
                'name': f'{address}_{owner}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]  
            }

            # Create the folder inside the specified parent folder
            folder = service.files().create(body=folder_metadata, fields='id').execute()

            # Output the new folder ID
            print('New Folder ID: %s' % folder.get('id'))
            request.session['property_folder_id'] = folder.get('id')
            request.session['owner'] = owner
            request.session['address'] = address

            # Redirect to the dashboard view after the form is processed
            return redirect('dashboard')
        

def dashboard_step_two_view(request):
    if request.method=="POST":
        # Assume you save the data here
        creds = get_google_credentials(request)

        # Build the Drive v3 API service
        service = build('drive', 'v3', credentials=creds)

        # Parent folder ID - ONBOARDING_AUTOMATION
        parent_folder_id = request.session['property_folder_id']

        owner = request.session['owner'] 
        address = request.session['address']

        folders_to_create = ['Owner','Property','Expenses']

        for folder_name in folders_to_create:
            # Define the folder metadata
            folder_metadata = {
                'name': f'{address}_{owner}_{folder_name}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]  
            }

            # Create the folder inside the specified parent folder
            folder = service.files().create(body=folder_metadata, fields='id').execute()

            if folder_name=="Owner":
                request.session['owner_folder_id'] = folder.get('id')
        
        return redirect('dashboard')

def dashboard_step_three_view(request):
    if request.method=="POST":
        creds = get_google_credentials(request)
        service = build('drive', 'v3', credentials=creds)

        owner_folder = request.session['owner_folder_id']


        bank_information_request = '1hOZUQ3r1dPi6_nOrHZTioQ4MlT8YXGox'
        service_agreement = '1RCPM2ReSEVa-TXLZs969sbWXj0gstozV'
        rental_agreement = '17uvFKKkvTS5a2lvrwYt-pc87Snxb_cxk'
        new_property_onboarding_template = '1u8I2DDT-2R-a0xXaRjTbAWo2VaAlzXvvm8yyQOs5bQk' #form
        w9_template = '1v3qzTASmbviM4jNxOEW2KZ0I6kz5vDeW'

        new_copies_ids = []

    document_ids = [bank_information_request,service_agreement,rental_agreement,new_property_onboarding_template,w9_template]

    for doc_id in document_ids:
        copy_metadata = {
            'parents': [owner_folder]  # Set the parent folder
        }

        # Create a copy of the document/form
        copied_file = service.files().copy(
            fileId=doc_id,
            body=copy_metadata,
            fields='id'
        ).execute()

        # Save the new copy ID
        new_copies_ids.append(copied_file['id'])

    # Handle post-copy logic or response
    print("Copied Files IDs:", new_copies_ids)
    return redirect('dashboard')

def dashboard_step_four_view(request):
    if request.method == "POST":  # Ensure the method check is correctly capitalized
        # Build the service
        creds = get_google_credentials(request)
        service = build('sheets', 'v4', credentials=creds)

        address = request.session.get('address')  # Safely retrieve 'address' from session
        owner = request.session['owner'] 

        # IDs and names
        spreadsheet_id = '1AxeYumE9OuGkzXluCduJzVSKilLFEz5EIbokH8Q9IQk'
        sheet_id_to_copy = '0'  # ID of the tab to be duplicated

        # Request to duplicate the sheet
        request_body = {
            'requests': [
                {
                    'duplicateSheet': {
                        'sourceSheetId': sheet_id_to_copy,
                        'insertSheetIndex': 1,  # Position where the new sheet should be inserted
                        'newSheetName': address  # Ensure the address is a valid sheet name
                    }
                }
            ]
        }
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request_body
        ).execute()

        # Get the ID of the newly created sheet
        new_sheet_id = response['replies'][0]['duplicateSheet']['properties']['sheetId']

        # Define the cell to update in the newly created sheet
        cell_range = f"{address}!B2"  # Correct range to target cell B1 in the new sheet

        # Fill the new sheet's B1 cell with specific data
        values = [[owner]]  # Data to be placed in B1
        body = {
            'values': values
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=cell_range,
            valueInputOption="USER_ENTERED",  # Changed to "USER_ENTERED" to interpret data correctly
            body=body
        ).execute()

        # Optionally, you can redirect or render a response here
        return redirect('dashboard')  



