from django.shortcuts import render, redirect, reverse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from django.contrib.auth.decorators import login_required
from .utils import get_google_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaInMemoryUpload
import io
import os
from googleapiclient.errors import HttpError

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
from django.shortcuts import render, get_object_or_404
from googleapiclient.discovery import build
from .utils import get_google_credentials
import uuid

from .models import OnboardingObject

@login_required
def onboarding_list(request):
    onboarding_objects = OnboardingObject.objects.all()
    return render(request, 'main.html', {'onboarding_objects': onboarding_objects})

def create_onboarding(request):
    new_onboarding = OnboardingObject.objects.create(
        id=uuid.uuid4(), 
        owner='',  
        address='',
        expenses_folder_id='',
        owner_folder_id='',
        property_folder_id='',
        onboarding_start_date=None,
        launch_date=None
    )
    return redirect('onboarding-detail', id=new_onboarding.id)

@login_required
def onboarding_detail(request, id):
    onboarding_object = get_object_or_404(OnboardingObject, id=id)
    # dashboard step one is now integrated directly.
    dashboard_step_one_form = DashboardStepOne()
    if request.method == 'POST':
            form = DashboardStepOne(request.POST)
            if form.is_valid():
                onboarding_object.address = form.cleaned_data['address']
                onboarding_object.owner = form.cleaned_data['owner']
                onboarding_object.onboarding_start_date = form.cleaned_data['start_date']
                onboarding_object.launch_date = form.cleaned_data['launch_date']
                onboarding_object.save()
                return redirect('onboarding-detail', id=onboarding_object.id)
    else:
        dashboard_step_one_form = DashboardStepOne(initial={
            'address': onboarding_object.address,
            'owner': onboarding_object.owner,
            'start_date': onboarding_object.onboarding_start_date,
            'launch_date': onboarding_object.launch_date
        })
    return render(request, 'dashboard.html', {'onboarding_object': onboarding_object,'dashboard_step_one_form': dashboard_step_one_form})


# owner onboarding folder - 1ub8g1ll4G0cNYb8OkqbJjwDIrRPHX5-7
# properties folder - 141hQMIqpuAXcwzvAczhiClzFvL-SGemb
# expenses folder - 1LRJmLgbAS339l9Q3IB-iEu0rA-yADlMy

def dashboard_step_two_view(request, id):
    if request.method=="POST":
        onboarding_object = get_object_or_404(OnboardingObject, id=id)
        # Assume you save the data here
        creds = get_google_credentials(request.user)

        # Build the Drive v3 API service
        service = build('drive', 'v3', credentials=creds)

        # acquire address and owner info from object
        address = onboarding_object.address
        owner = onboarding_object.owner 

        # OWNER FOLDER
        parent_folder_id = '1ub8g1ll4G0cNYb8OkqbJjwDIrRPHX5-7'

        folder_metadata = {
                'name': owner,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]  
            }

        # Create the folder inside the specified parent folder
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        onboarding_object.owner_folder_id = folder.get('id')

        # PROPERTY FOLDER
        parent_folder_id = '141hQMIqpuAXcwzvAczhiClzFvL-SGemb'

        folder_metadata = {
                'name': address,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]  
            }

        # Create the folder inside the specified parent folder
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        onboarding_object.property_folder_id = folder.get('id')

        # EXPENSES FOLDER
        parent_folder_id = '1LRJmLgbAS339l9Q3IB-iEu0rA-yADlMy'

        folder_metadata = {
                'name': f'{address} [Expenses]',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]  
            }

        # Create the folder inside the specified parent folder
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        onboarding_object.expenses_folder_id = folder.get('id')

        onboarding_object.save()

        url = reverse('onboarding-detail', kwargs={'id': id})

        return redirect(url)

def dashboard_step_three_view(request, id):
    if request.method=="POST":
        onboarding_object = get_object_or_404(OnboardingObject, id=id)
        creds = get_google_credentials(request.user)
        drive_service = build('drive', 'v3', credentials=creds)
        forms_service = build('forms', 'v1', credentials=creds)


        new_copies_ids = []

        address = onboarding_object.address
        owner = onboarding_object.owner 


        document_ids = {}
        document_ids['Rental Agreement - '] = '1QYq1h4fH0FUzVTw02XEcNyDN35w9yjfLOduOS8mgXoQ'
        document_ids['TEN PERCENT Destination UX Services Agreement - '] = '1ImNYdWTfAx6AuSmyRV8RaF3M3Nzly0zQ'
        document_ids['W9 - '] = '1v3qzTASmbviM4jNxOEW2KZ0I6kz5vDeW'
        document_ids['Bank Information Request Form - '] = '1hOZUQ3r1dPi6_nOrHZTioQ4MlT8YXGox'
        document_ids['New Owner & Property Onboarding Template - '] = '1tmJYZKIKYtdfVe6q6AH1TeXNtyDOx5vdapk7TJeRqa4'

        owner_folder = onboarding_object.owner_folder_id

        for name,doc_id in document_ids.items():
            copy_metadata = {
                'name': f'{name}{owner}',
                'parents': [owner_folder] 
            }

            # Create a copy of the document/form
            copied_file = drive_service.files().copy(
                fileId=doc_id,
                body=copy_metadata,
                fields='id'
            ).execute()

            # Save the new copy ID
            new_copies_ids.append(copied_file['id'])

        # Handle post-copy logic or response
        print("Copied Files IDs:", new_copies_ids)
        url = reverse('onboarding-detail', kwargs={'id': id})

        return redirect(url)

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



