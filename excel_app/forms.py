from django import forms


class UploadFileForm(forms.Form):
    customer_details = forms.FileField()

    def __str__(self):
        return self.title
