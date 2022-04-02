from django import forms
from django.forms import ModelForm
from .models import UploadCsvModel

class UploadCsvModelForm(forms.ModelForm):
    product = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Catalog File', 'accept':'.csv', 'class':'form-control py-2', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = UploadCsvModel
        fields = ('product',)


class GetKeyForm(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('appkey', 'secretkey',)

class UploadProductCatalogForm(forms.Form):
    productcatalog = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Product Catalog', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('productcatalog', 'appkey', 'secretkey',)


 