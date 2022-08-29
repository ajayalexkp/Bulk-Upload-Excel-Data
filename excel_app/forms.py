from django import forms


class UploadFileForm(forms.Form):
    customer_details = forms.FileField()


