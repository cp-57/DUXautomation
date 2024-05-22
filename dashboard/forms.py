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

# class DashboardStepTwo(forms.Form):
#     files = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'multiple': True}),
#         label="Select files",
#         required=False
#     )
    