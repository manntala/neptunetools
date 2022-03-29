from django import forms
from django.forms import ModelForm
from .models import ReviewRating

class GetKeyForm(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    class Meta:
        fields = ('appkey', 'secretkey',)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'name', 'email', 'review', 'rating']

class BuyForm(forms.Form):
    order_external_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    order_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    cs_external_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    cs_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    product_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('order_external_id', 'order_date', 'cs_external_id', 'cs_email', 'first_name', 'last_name', 'product_id', 'quantity',)