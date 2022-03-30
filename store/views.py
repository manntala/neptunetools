from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from .forms import GetKeyForm, GetKeyForm2

def symbol_remove(string):
    replaced = string.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('"', '').replace('\'', '').replace(':', ' ').replace(',', '').replace('errors', '').replace('error', '').replace('message', '')
    return replaced.title()

@login_required
def removetoken(request):
    form = GetKeyForm()
    context = {
        'nav_store1_active': True,
        'form': form,
    }

    if request.method == 'POST':
        form = GetKeyForm(request.POST)
        if form.is_valid():
            appkey = form.cleaned_data['appkey']
            secretkey = form.cleaned_data['secretkey']

            payload = {
            "client_id": appkey,
            "client_secret": secretkey,
            "grant_type": "client_credentials"
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            url = 'https://api.yotpo.com/oauth/token'
            response = requests.request("GET", url=url, json=payload, headers=headers)
            utoken = response.json()['access_token']

            context = {
                'utoken': response.json()['access_token'],
                'nav_store1_active': True,
                }      

            url = f"https://api.yotpo.com/apps/{appkey}/account_platform"

            payload = {
                    "account_platform": {
                        "shop_token": "",
                        "shop_secret": "",
                        "shop_domain": "",
                        },
                    "utoken": utoken
                    }
                    
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.request("PUT", url, json=payload, headers=headers)

            print(response.text)
            if response.status_code == 200:
                messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + ' Token Removed!')
                return render(request, 'store/removetoken.html', context)
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + ' Invalid Credentials')
                return render(request, 'store/removetoken.html', context)

    return render(request, 'store/removetoken.html', context)


@login_required
def addtoken(request):
    form = GetKeyForm2()
    context = {
        'nav_addtoken_active': True,
        'form': form,
    }

    if request.method == 'POST':
        form = GetKeyForm2(request.POST)
        if form.is_valid():
            appkey = form.cleaned_data['appkey']
            secretkey = form.cleaned_data['secretkey']

            shop_token = request.POST.get('shop_token')
            shop_domain = request.POST.get('shop_domain')

            payload = {
            "client_id": appkey,
            "client_secret": secretkey,
            "grant_type": "client_credentials"
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            url = 'https://api.yotpo.com/oauth/token'
            response = requests.request("GET", url=url, json=payload, headers=headers)
            utoken = response.json()['access_token']

            context = {
                'utoken': response.json()['access_token'],
                'nav_addtoken_active': True,
                }      

            url = f"https://api.yotpo.com/apps/{appkey}/account_platform"

            payload = {
                    "account_platform": {
                        "shop_token": shop_token,
                        "shop_domain": shop_domain,
                        },
                    "utoken": utoken
                    }
                    
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.request("PUT", url, json=payload, headers=headers)

            print(response.text)
            if response.status_code == 200:
                messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + ' Shop Token and Domain Updated')
                return render(request, 'store/addtoken.html', context)
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + ' Invalid Credentials')
                return render(request, 'store/addtoken.html', context)

    return render(request, 'store/addtoken.html', context)    

def storeview(request):
    form = GetKeyForm()
    context = {
        'nav_store2_active': True,
        'form': form,
    }

    if request.method == 'POST':
        form = GetKeyForm(request.POST)
        if form.is_valid():
            appkey = form.cleaned_data['appkey']
            secretkey = form.cleaned_data['secretkey']

            payload = {
            "client_id": appkey,
            "client_secret": secretkey,
            "grant_type": "client_credentials"
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            url = 'https://api.yotpo.com/oauth/token'
            response = requests.request("GET", url=url, json=payload, headers=headers)
            utoken = response.json()['access_token']

            context = {
                'utoken': response.json()['access_token'],
                }      

            url = f"https://api.yotpo.com/apps/{appkey}/account_platform"

            payload = {
   
                    "utoken": utoken
                    }
                    
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.request("GET", url, json=payload, headers=headers)
            output = response.json()['response']
            

            context = {               
                'response': output,
                'nav_store2_active': True
            }

            print(response.text)
            if response.status_code == 200:
                messages.add_message(request, messages.SUCCESS, 'Account Platform Status')
                return render(request, 'store/storeview.html', context)
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + ' Invalid Credentials')
                return render(request, 'store/storeview.html', context)


    return render(request, 'store/storeview.html', context)




