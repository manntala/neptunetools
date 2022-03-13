from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from .forms import GetKeyForm, GetKeyForm2

def symbol_remove(string):
    replaced = string.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('"', '').replace('\'', '').replace(':', ' ').replace(',', '').replace('errors', '').replace('error', '').replace('message', '')
    return replaced.title()

@login_required
def storeupdate(request):
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

            shop_token = form.cleaned_data['shop_token']
            shop_domain = form.cleaned_data['shop_domain']

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
                    "account_platform": {
                        "shop_token": shop_token,
                        "shop_secret": "",
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
                messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + ' Platform Updated!')
                return render(request, 'store/storeupdate.html', context)
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + ' Invalid Credentials')
                return render(request, 'store/active.html', context)

    return render(request, 'store/storeupdate.html', context)

def storeview(request):
    form = GetKeyForm2()
    context = {
        'nav_store2_active': True,
        'form': form,
    }

    if request.method == 'POST':
        form = GetKeyForm2(request.POST)
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
            print(output)

            context = {               
                'response': output
            }

            print(response.text)
            if response.status_code == 200:
                messages.add_message(request, messages.SUCCESS, 'Success!')
                return render(request, 'store/storeview.html', context)
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + ' Invalid Credentials')
                return render(request, 'store/storeview.html', context)


    return render(request, 'store/storeview.html', context)




