from django import forms

class GetKeyForm(forms.Form):
    appkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))
    secretkey = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control', }))

    class Meta:
        fields = ('appkey', 'secretkey',)

        