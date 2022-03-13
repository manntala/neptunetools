from django import forms

class GetKeyForm(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    shop_token = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    shop_domain = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('appkey', 'secretkey', 'shop_token', 'shop_domain')

class GetKeyForm2(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('appkey', 'secretkey',)