from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import requests
import json

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard/index.html')

def getkey(request, appkey, secretkey):

    payload = {
            "secret": secretkey
        }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    url = f'https://api.yotpo.com/core/v3/stores/{appkey}/access_tokens'
    response = requests.request("POST", url=url, json=payload, headers=headers)
    utoken = response.json()['access_token']

    return utoken
            

