from django import forms
from django.forms import ModelForm
from .models import UploadCsvModel

class UploadCsvModelForm(forms.ModelForm):
    product = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Catalog File', 'accept':'.csv', 'class':'form-control py-2', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = UploadCsvModel
        fields = ('product',)

 