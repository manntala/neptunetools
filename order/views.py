from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required

from rest_framework import serializers
from rest_framework import permissions
from .forms import OrderProcessForm, CsvModelForm, GetKeyForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.conf import settings
from pathlib import Path

from rest_framework import generics
from .models import Post, Csv, OrderProcessModel, GetKey

from django.contrib.auth.decorators import login_required

# third party imports
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, OrderProcessSerializer

from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, OrderProcessSerializer
from .models import OrderProcessModel, OrderTemplate

import pandas as pd 
import re
import mimetypes
import os
import requests
import json


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path

import uuid

def symbol_remove(string):
    replaced = string.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('"', '').replace('\'', '').replace(':', ' ').replace(',', '').replace('errors', '').replace('error', '').replace('message', '')
    return replaced.title()

def home(request):
    return render(request, 'order/home.html')

class PostView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def get(self, request, *args, **kwargs):
        
        return Response(serializers.data)
    
@login_required 
def uploadcsv(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        fs = form.save(commit=False)
        fs.owner = request.user
        fs.identifier = uuid.uuid4()
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(identifier=fs.identifier)
        with open(obj.file_name.path, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            review_count = 0
            for i, row in enumerate(reader):
                review_count += 1
                print(i)
                if i==0:
                    pass
                else:
                    OrderProcessModel.objects.create(
                    order_id=row[0],
                    order_date=row[1],
                    external_id=row[2],
                    email=row[3],
                    first_name=row[4],
                    last_name=row[5],
                    quantity=row[6],
                    product_id=row[7],
                    owner=request.user
                    )
                    print(row)
            obj.activated = True
            obj.save()
        
        messages.success(request, f'' + str(review_count-1) + ' ' + 'Record/s Added!')
        return redirect(to='send')
        # return render(request, 'order/dashboard.html', {'review_count': review_count})
    
    return render(request, 'order/send.html', {'form': form})

@login_required
def dashboard(request):
    template = OrderTemplate.objects.latest('id')
    form = CsvModelForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'template': template
    }
    return render(request, 'order/send.html', context)

@login_required
def download(request,path):
    file_path = (settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/csv')
            response['Content-Disposition'] = 'inline;filename='+os.path.basename(file_path)
            return response
@login_required
def activate(request, id):
    not_selected = GetKey.objects.all().exclude(id=id) # get all the objects that are not selected
    selected = GetKey.objects.get(id=id) # get the selected object

    selected.active = True
    not_selected.active = False

    for i in not_selected:
        i.active = False
        i.save()

    selected.save()
    if selected:
        messages.success(request, f'{selected.appkey} Activated!')
        return redirect('gettoken')

@login_required
def deactivate(request, id):
    selected = GetKey.objects.get(id=id) # get the selected object


    selected.active = False
    selected.save()
    if selected:
        messages.success(request, f'{selected.appkey} Deactivated!')
        return redirect('gettoken')

@login_required
def send(request):
    form = CsvModelForm()
    template = OrderTemplate.objects.get(pk=1)
    file_path = 'media/save'
    context = {
        'form': form,
        'template': template,
        'file_path': file_path
    }
    # order_processes = get_list_or_404(OrderProcessModel)
    # serializer = OrderProcessSerializer(order_processes, many=True)

    if request.method == 'POST':
        key = GetKey.objects.filter(owner=request.user).filter(active=True)

        if key:
            messages.success(request, f'App Key: {key[0].appkey}')

            appkey = key[0].appkey
            secretkey = key[0].secretkey

            HttpResponse(appkey, secretkey)
            
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
            # context = {
            #     'utoken': response.json()['access_token']
            #     }       
            # messages.add_message(request, messages.INFO, f'{utoken}')
        
            if utoken:
                order_processes = OrderProcessModel.objects.filter(owner=request.user).filter(sent=False)
                serializer = OrderProcessSerializer(order_processes, many=True)

                for i in serializer.data:
                    print(i)
                                
                    payload = { "order": {
                                "external_id": i['order_id'],
                                "order_date": i['order_date'],
                                "customer": {
                                    "external_id": i['external_id'],
                                    "email": i['email'],
                                    "first_name": i['first_name'],
                                    "last_name": i['last_name']
                                },
                                "line_items": [
                                    {
                                        "quantity": i['quantity'],
                                        "external_product_id": i['product_id']
                                    }
                                ],
                                "fulfillments": [
                                {
                                    "fulfillment_date": i['order_date'],
                                    "external_id": i['order_id'],
                                    "status": "success",
                                    "fulfilled_items": [
                                        {
                                            "external_product_id": i['product_id'],
                                            "quantity": i['quantity']
                                        }
                                    ]
                                }
                            ]
                            }}

                    headers = {
                        "X-Yotpo-Token": f"{utoken}",
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                        }
                    
                    url = f"https://api.yotpo.com/core/v3/stores/{appkey}/orders"

                    response = requests.request("POST", url=url, json=payload, headers=headers)
                    print(response.text)

                    

                    
                if response.status_code == 201:
                    messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + '!')   
                    return redirect(to='send') 
                    delete = OrderProcessModel.objects.filter(owner=request.user).delete()
                elif response.status_code == 400:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')  
                    return redirect(to='send')  
                    delete = OrderProcessModel.objects.filter(owner=request.user).delete()
                elif response.status_code == 409:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')   
                    return redirect(to='send') 
                    delete = OrderProcessModel.objects.filter(owner=request.user).delete()
                else:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')
                    return redirect(to='send')
                    delete = OrderProcessModel.objects.filter(owner=request.user).delete()
                  
                    
                     
                # else:
                #     messages.add_message(request, messages.ERROR, 'Invalid CSV!')
                #     return redirect(to='send')

            else:
                messages.add_message(request, messages.ERROR, 'Please Add/Activate your AppKey/SecretKey!')
                return redirect(to='send')

        else:
            messages.error(request, f'Please select an appkey!')
            return redirect(to='send')
   
    # end of post
    else:      
        return render(request, 'order/send.html', context)

@login_required
def display(request):
    key = GetKey.objects.filter(owner=request.user).filter(active=True)

    if key:
        messages.success(request, f'{key[0].appkey} is Selected!')

        appkey = key[0].appkey
        secretkey = key[0].secretkey

        HttpResponse(appkey, secretkey)
        
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

        
        if utoken:
            url = f"https://api.yotpo.com/core/v3/stores/{appkey}/orders"

            headers = {
                "X-Yotpo-Token": f"{utoken}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("GET", url=url, headers=headers)
            if response:
                orders = response.json()['orders']
                context = {
                    'orders': orders,
                    'appkey': appkey,
                    'secretkey': secretkey
                }
                return render(request, 'order/display.html', context)
            else:
                messages.add_message(request, messages.ERROR, 'No orders found!')
                return redirect(to='order/display')
        
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Token!')
            return redirect(to='order/display')

    messages.add_message(request, messages.ERROR, 'Please Add/Activate your AppKey/SecretKey!')
    return render(request, 'order/display.html')

@login_required
def displayid(request, id):
    key = GetKey.objects.filter(owner=request.user).filter(active=True)
    order_id = id

    if key:
            # messages.success(request, f'{key[0].appkey} is Selected!')

            appkey = key[0].appkey
            secretkey = key[0].secretkey

            HttpResponse(appkey, secretkey)
            
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

            if utoken:
                url = f"https://api.yotpo.com/core/v3/stores/{appkey}/orders/{order_id}"

                headers = {
                    "X-Yotpo-Token": f"{utoken}",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

                response = requests.request("GET", url=url, headers=headers)
                if response:
                    order = response.json()['order']
                   
                    context = {
                        'order': order
                    }
                    return render(request, 'order/displayid.html', context)
                else:
                    messages.add_message(request, messages.ERROR, 'Invalid Order ID!')
                    return redirect('displayid', id)
    
    return redirect('displayid', id)

@login_required
def view_catalog(request):
    if request.method == 'POST':
        appkey = request.POST.get('appkey')
        secretkey = request.POST.get('secretkey')
        
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
            'utoken': response.json()['access_token']
            }       
        messages.add_message(request, messages.INFO, f'Token: '+utoken)
        
        if utoken:
            url = f"https://api.yotpo.com/core/v3/stores/{appkey}/products"

            headers = {
                "X-Yotpo-Token": f"{utoken}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("GET", url=url, headers=headers)
            data = response.json()['products']
            

            product_list = []
            for item in data:
                
                product_id = data[0]['external_id']
                product_name = data[0]['name']
                product_url = data[0]['url']
                product_image_url = data[0]['image_url']
                product_price = data[0]['price']
                product_currency = data[0]['currency']
                product_mpn = data[0]['mpn']
                product_brand = data[0]['brand']
                # product_isbn = data[0]['isbn']
                product_upc = data[0]['gtins']
                product_sku = data[0]['sku']
                # product_tags = data[0]['tags']
                product_blacklisted = data[0]['is_discontinued']
                product_group = data[0]['group_name']
                

                products = {
                    'Product ID': product_id,
                    'Product Name': product_name,
                    'Product URL': product_url,
                    'Product Image URL': product_image_url,
                    'Product Price': product_price,
                    'Currency': product_currency,
                    'Spec UPC': product_upc,
                    'Spec MPN': product_mpn,
                    'Spec Brand': product_brand,
                    # 'Spec ISBN': product_isbn,
                    'Spec SKU': product_sku,
                    # 'Product Tags': product_tags,
                    'Blacklisted': product_blacklisted,
                    'Product Group': product_group 
                }
                product_list.append(products)

            url_df = pd.DataFrame(product_list, columns=['Product ID', 'Product Name', 'Product URL', 'Product Image URL', 'Product Price', 'Currency', 'Spec UPC', 'Spec MPN', 'Spec Brand', 'Spec ISBN', 'Spec SKU', 'Product Tags', 'Blacklisted', 'Product Group'])
            


            tmp_name = str(uuid.uuid4())
            file_path = 'static/tmp/'+tmp_name+'/'
            file_path = makedirs(file_path)
            url_df.to_csv(file_path+'product_catalog_v3.csv', index=False)
            
            context = {
                'file_path': file_path+'product_catalog_v3.csv',
                'file_name': 'product_catalog_v3.csv',
                
            }

            messages.add_message(request, messages.INFO, 'Product Catalog Downloaded!')
            return render(request, 'order/view_catalog.html', context)
        
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Token!')
            return redirect('/view-catalog/#view-catalog')

    
    return render(request, 'order/view_catalog.html')

@login_required     
def gettoken(request):
    form = GetKeyForm()
    context = {
        'form': form,
        'keys': GetKey.objects.filter(owner=request.user)
        }

    if request.method == 'POST':

        form = GetKeyForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.owner = request.user

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
                'utoken': response.json()['access_token']
                }      

            fs.token = utoken
            form.save()
            messages.add_message(request, messages.INFO, 'Token Saved!')
            return redirect('gettoken')
        else:
            messages.add_message(request, messages.ERROR, 'Appkey is already in use!')
            return render(request, 'order/gettoken.html', context)
    else:
        return render(request, 'order/gettoken.html', context)

    return render(request, 'order/gettoken.html', context)
    

# functions not in used 

@login_required   
class OrderProcessView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        order_processes = get_list_or_404(OrderProcessModel)
        serializer = OrderProcessSerializer(order_processes, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = OrderProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error_messages)
    
@login_required
def catalogUpload(request):
    form = CatalogUploadForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        fs = form.save(commit=False)
        fs.owner = request.user
        fs.identifier = uuid.uuid4()
        form.save()
        form = CatalogUploadForm()
        obj = Csv.objects.get(identifier=fs.identifier)
        with open(obj.file_name.path, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            review_count = 0
            for i, row in enumerate(reader):
                review_count += 1
                print(i)
                if i==0:
                    pass
                else:
                    OrderProcessModel.objects.create(
                    order_id=row[0],
                    order_date=row[1],
                    external_id=row[2],
                    email=row[3],
                    first_name=row[4],
                    last_name=row[5],
                    quantity=row[6],
                    product_id=row[7],
                    owner=request.user
                    )
                    print(row)
            obj.activated = True
            obj.save()
        
        messages.success(request, f'' + str(review_count-1) + ' ' + 'records added')
        return redirect(to='/dashboard#dashboard')
        # return render(request, 'order/dashboard.html', {'review_count': review_count})
    
    return render(request, 'order/dashboard.html', {'form': form})

@login_required
def resetorder(request):
    form =  CsvModelForm()
    context = {
    'form' : form
    }
    return render(request, "order/send.html", context)


def downloadtemplate(request):
    template = OrderTemplate.objects.get(pk=1)
    return render(request, 'order/send.html', {'template': template})

def cancelorder(request):
    try:
        order = OrderProcessModel.objects.filter(owner=request.user).delete()
        return redirect(to='send')
    except:
        return redirect(to='send')  
        
    return redirect(to='send')
