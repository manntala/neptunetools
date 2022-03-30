from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from account.models import Account, Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.', widget= forms.TextInput (attrs={'placeholder':''}))
    username = forms.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', widget= forms.TextInput (attrs={'placeholder':''}))
    first_name= forms.CharField(max_length=100, widget= forms.TextInput (attrs={'placeholder':''}))
    last_name= forms.CharField(max_length=100, widget= forms.TextInput (attrs={'placeholder':''}))
    password1 = forms.CharField(label='Password', widget= forms.PasswordInput(attrs={'placeholder':''}))
    password2 = forms.CharField(label='Password confirmation', widget= forms.PasswordInput(attrs={'placeholder':''}))


    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AccountAuthenticationForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.TextInput (attrs={'placeholder':''}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput (attrs={'placeholder':''}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            try:
                account = Account.objects.get(email=email)
                if account.check_password(password):
                    return self.cleaned_data
                else:
                    self._errors['password'] = self.error_class(['Incorrect password'])

            except Account.DoesNotExist:
                self._errors['email'] = self.error_class(['Email does not exist'])
    
    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name']

    # def clean_email(self):
    #     if self.is_valid():
    #         email = self.cleaned_data['email']
    #         try:
    #             account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
    #         except Account.DoesNotExist:
    #             return email
    #         raise forms.ValidationError('Email "%s" is already in use.' % email)
    
    # def clean_username(self):
    #     if self.is_valid():
    #         username = self.cleaned_data['username']
    #         try:
    #             account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
    #         except Account.DoesNotExist:
    #             return username
    #         raise forms.ValidationError('Username "%s" is already in use.' % username)
    
    
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs = {
        #     'id': 'username', 'class': 'form-control', 'placeholder': 'Username', 'type': 'text'}
        self.fields['first_name'].widget.attrs = {
            'id': 'firstName', 'class': 'form-control py-2', 'placeholder': 'First Name', 'type': 'text'}
        self.fields['last_name'].widget.attrs = {
            'id': 'lastName', 'class': 'form-control py-2', 'placeholder': 'Last Name', 'type': 'text'}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs = {
            'id': 'customFile', 'class': 'form-control py-2', 'name': 'image', 'type': 'file'}
        
    

            