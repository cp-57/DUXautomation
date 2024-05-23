from django import forms

class DashboardStepOne(forms.Form):
    address = forms.CharField(
        label="Address",  
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the address'})
    )
    owner = forms.CharField(
        label="Owner",  
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the owner(s) name(s)'})
    )
    start_date = forms.DateField(
        label="Onboarding Start Date",
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select the onboarding start date'})
    )
    launch_date = forms.DateField(
        label="Launch Date",
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select the target launch date'})
    )

# class DashboardStepTwo(forms.Form):
#     files = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'multiple': True}),
#         label="Select files",
#         required=False
#     )
    