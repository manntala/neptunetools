from django import forms
from django.forms import ModelForm
from .models import UploadedCSVModel
from order.models import Csv

class CatalogUploadForm(forms.ModelForm):
    file_name = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Product Catalog', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = Csv
        fields = ('file_name',)

class ReviewsUploadCatalog(forms.ModelForm):
    file_name = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Import File', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = Csv
        fields = ('file_name',)

class UploadedCSVModelForm(forms.ModelForm):
    catalog = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Product Catalog.', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))
    reviews = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Import File', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = UploadedCSVModel
        fields = ('catalog', 'reviews')

# used

class UploadDataForm(forms.Form):
    catalog = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Product Catalog', 'accept':'.csv', 'class':'form-control py-2', 'onchange':'triggerValidation(this)'}))
    reviews = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Import File', 'accept':'.csv', 'class':'form-control py-2', 'onchange':'triggerValidation(this)'}))

    class Meta:
        fields = ('catalog', 'reviews')

class UploadScraperForm(forms.Form):
    shopifyurl = forms.URLField(label='Shopify URL', widget=forms.TextInput(attrs={'placeholder':'https://shopifyurl.com/', 'class':'form-control py-2', }))
    reviews = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload Import File', 'accept':'.csv', 'class':'form-control py-2', 'onchange':'triggerValidation(this)'}))

    class Meta:
        fields = ('shopifyurl', 'reviews')

 