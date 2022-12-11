from django import forms
from django.forms import ModelForm
from .models import Csv, OrderProcessModel, GetKey, OrderUpdateModel

class OrderProcessForm(forms.ModelForm):
    class Meta:
        model = OrderProcessModel
        fields = ('email', 'first_name', 'last_name', 'order_id', 'order_date',)
        
class CsvModelForm(forms.ModelForm):
    file_name = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload CSV file', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = Csv
        fields = ('file_name',)


class GetKeyForm(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('appkey', 'secretkey',)

class CsvUpdateOrderModelForm(forms.ModelForm):
    file_name = forms.FileField(widget=forms.FileInput(attrs={'placeholder':'Upload CSV file', 'accept':'.csv', 'class':'form-control', 'onchange':'triggerValidation(this)'}))

    class Meta:
        model = Csv
        fields = ('file_name',)
        