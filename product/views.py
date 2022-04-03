from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from order.models import GetKey
from .models import UpdateProductModel, UploadCsvModel, AddProductModel
from .forms import UploadCsvModelForm, GetKeyForm, UploadProductCatalogForm

from dashboard.views import getkey

from .serializers import UpdateProductModelSerializer, AddProductModelSerializer

import requests
import pandas as pd 
import numpy as np
import json
import uuid
import csv
import os

# save to csv
from io import StringIO # python3; python2: BytesIO 
import boto3
from django.conf import settings


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path

# copy to s3
s3 = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
def copy_to_s3(client, df, bucket, filepath):
        csv_buf = StringIO()
        df.to_csv(csv_buf, header=True, index=False)
        csv_buf.seek(0)
        client.put_object(Bucket=bucket, Body=csv_buf.getvalue(), Key=filepath)
        # print(f'Copy {df.shape[0]} rows to S3 Bucket {bucket} at {filepath}, Done!')

def symbol_remove(string):
    replaced = string.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('"', '').replace('\'', '').replace(':', ' ').replace(',', '').replace('errors', '').replace('error', '').replace('message', '')
    return replaced.title()

@login_required
def catalogdisplay(request):

    if request.method == 'POST':
        keyform = GetKeyForm(request.POST)

        if keyform.is_valid():
            appkey = keyform.cleaned_data['appkey']
            secretkey = keyform.cleaned_data['secretkey']

            utoken = getkey(request, appkey, secretkey)
        
            if utoken:
                url = f"https://api.yotpo.com/core/v3/stores/{appkey}/products"
                

                headers = {
                    "X-Yotpo-Token": f"{utoken}",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                response = requests.request("GET", url=url, headers=headers)
                data = response.json()
                

                catalog_list = []
                for item in data['products']:

                    yotpo_id = item['yotpo_id']
                    product_id = item['external_id']
                    product_name = item['name']
                    product_url = item['url']
                    product_image_url = item['image_url']
                    product_price = item['price']
                    product_currency = item['currency']
                    product_mpn = item['mpn']
                    product_brand = item['brand']
                    # product_isbn = item['isbn']
                    try :
                        product_upc = item['gtins'][0]['value']
                    except:
                        product_upc = 'null'
                    # product_upc = item['gtins'][0]['value'] if item['gtins'][0]['value'] == 'null' else item['gtins'][0]['value']
                    product_sku = item['sku']
                    # product_tags = item['tags']
                    product_blacklisted = item['is_discontinued']
                    product_group = item['group_name']

                    

                    catalog = {
                        'Yotpo ID': yotpo_id,
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
                    catalog_list.append(catalog)

                url_df = pd.DataFrame(catalog_list, columns=['Yotpo ID', 'Product ID', 'Product Name', 'Product URL', 'Product Image URL', 'Product Price', 'Currency', 'Spec UPC', 'Spec MPN', 'Spec Brand', 'Spec ISBN', 'Spec SKU', 'Product Tags', 'Blacklisted', 'Product Group'])
            
                
                tmp_name = str(uuid.uuid4())
                file_path = 'static/tmp/'+tmp_name+'/'+'product_catalog.csv'
                
                copy_to_s3(client=s3, df=url_df, bucket='neptunestatic', filepath=file_path)  
                
                context = {
                    'keyform': GetKeyForm(),
                    'file_path': file_path,
                    'file_name': 'product_catalog_v3.csv',
                    'nav_prod1_active': True
                    
                }

                messages.add_message(request, messages.INFO, 'Product Catalog Downloaded!')
                return render(request, 'product/catalogdisplay.html', context)
        
            else:
                messages.add_message(request, messages.ERROR, 'Invalid Token!')
                return redirect(to='catalogdisplay')

    context = {
        'file_path': '',
        'nav_prod1_active': True,
        'keyform': GetKeyForm(),
    }
    return render(request, 'product/catalogdisplay.html', context)

@login_required
def createproduct(request):
    key = GetKey.objects.filter(owner=request.user).filter(active=True)
    appkey = key[0].appkey
    secretkey = key[0].secretkey
    utoken = key[0].utoken

    url = f"https://api.yotpo.com/core/v3/stores/{appkey}/products"

    payload = {
                "product": {
                    "external_id": "ak123798684325sdfkj",
                    "name": "minimal surfboard",
                    "description": "A great surfboard!",
                    "url": "http://www.waverider.com/products/minimalsurfboard",
                    "price": 750,
                    "sku": "xxxxx"
                }
            }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

    return render(request, 'product/createproduct.html')

@login_required
def resetproduct(request):

    context = {
    'form' : UploadProductCatalogForm(),
    'file_path': '',
    }
    return render(request, "product/catalogupdate.html", context)

@login_required
def resetaddproduct(request):

    context = {
    'form' : UploadProductCatalogForm(),
    'file_path': '',
    }
    return render(request, "product/catalogadd.html", context)

@login_required
def resetproductdisplay(request):
    keyform =  GetKeyForm()
    context = {
        'nav_prod1_active': True,
        'keyform' : keyform,
        'file_path': '',
    }
    return render(request, "product/catalogdisplay.html", context)

@login_required
def uploadproductcatalog(request):
    form = UploadCsvModelForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        fs = form.save(commit=False)
        fs.owner = request.user
        fs.identifier = uuid.uuid4()
        form.save()
        form = UploadCsvModelForm()
        obj = UploadCsvModel.objects.get(identifier=fs.identifier)
        with open(obj.product.path.name, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            review_count = 0
            for i, row in enumerate(reader):
                review_count += 1
                print(i)
                if i==0:
                    pass
                else:
                    UpdateProductModel.objects.create(
                    yotpo_id=row[0],
                    external_id=row[1],
                    product_title=row[2],
                    product_url=row[3],
                    product_image_url=row[4],
                    product_price=row[5] if row[5] else None,
                    product_currency=row[6],
                    upc=row[7],
                    mpn=row[8],
                    brand=row[9],
                    isbn=row[10],
                    sku=row[11],
                    product_tags=row[12],
                    blacklisted=row[13].title(),
                    product_group=row[14],
                    processed = False,
                    owner=request.user,

                    )
                    print(row)
            obj.activated = True
            obj.save()
        
        messages.success(request, f'' + str(review_count-1) + ' ' + 'Record/s Added!')
        return redirect(to='catalogupdate')
    
    return render(request, 'product/catalogupdate.html', {'form': form})

@login_required
def uploadaddcatalog(request):
    form = UploadCsvModelForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        fs = form.save(commit=False)
        fs.owner = request.user
        fs.identifier = uuid.uuid4()
        form.save()
        form = UploadCsvModelForm()
        obj = UploadCsvModel.objects.get(identifier=fs.identifier)
        with open(obj.product.path.name, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            review_count = 0
            for i, row in enumerate(reader):
                review_count += 1
                print(i)
                if i==0:
                    pass
                else:
                    AddProductModel.objects.create(
                    
                    external_id=row[0],
                    product_title=row[1],
                    description=row[2],
                    product_url=row[3],
                    product_price=row[4] if row[5] else None,
                    sku=row[5],
                    processed = False,
                    owner=request.user,

                    )
                    print(row)
            obj.activated = True
            obj.save()
        
        messages.success(request, f'' + str(review_count-1) + ' ' + 'Record/s Added!')
        return redirect(to='catalogadd')
    
    return render(request, 'product/catalogadd.html', {'form': form})

@login_required
def catalogupdate(request):
    context = {
        'file_path': '',
        'form': UploadProductCatalogForm(),
        'nav_prod3_active': True
    }
    if request.method == 'POST':

        form = UploadProductCatalogForm(request.POST, request.FILES or None)
        if form.is_valid():
    
            appkey = form.cleaned_data['appkey']
            secretkey = form.cleaned_data['secretkey']
            products = form.cleaned_data['productcatalog']

            products_df = pd.read_csv(products)
            products_df = products_df.fillna({'Spec UPC': 'Null'})
            products_df = products_df.fillna({'Blacklisted': 'False'})
            products_df.fillna('', inplace=True)


            for i, row in products_df.iterrows():
                
                UpdateProductModel.objects.create(
                    yotpo_id=row[0],
                    external_id=row[1],
                    product_title=row[2],
                    product_url=row[3],
                    product_image_url=row[4],
                    product_price=row[5],
                    product_currency=row[6],
                    upc=row[7],
                    mpn=row[8],
                    brand=row[9],
                    isbn=row[10],
                    sku=row[11],
                    product_tags=row[12],
                    blacklisted=row[13],
                    product_group=row[14],
                    processed = False,
                    owner=request.user,

                )

            utoken = getkey(request, appkey, secretkey)

            if utoken:
                data = UpdateProductModel.objects.filter(owner=request.user).filter(processed=False)
                serializer = UpdateProductModelSerializer(data, many=True)
                

                for i in serializer.data:
                    yotpo_id = i['yotpo_id']

                    payload = {"product": {
                                    "external_id": i['external_id'],
                                    "name": i['product_title'],
                                    "url": i['product_url'],
                                    "image_url": i['product_image_url'],
                                    "price": i['product_price'],
                                    "currency": i['product_currency'],
                                    "is_discontinued": "false", 
                                    "group_name": i['product_group'],
                                    "brand": i['brand'],
                                    "sku": i['sku'],
                                    "mpn": i['mpn'],
                                    "isbn": i['isbn'],
                                    "gtins": [
                                        {
                                            "declared_type": "UPC",
                                            "value": i['upc'] 
                                        },

                                    ]
                        }}

                    headers = {
                        "X-Yotpo-Token": utoken,
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                        }
                    
                    url = f"https://api.yotpo.com/core/v3/stores/{appkey}/products/{yotpo_id}"
                    

                    response = requests.request("PATCH", url=url, json=payload, headers=headers)
                    delete = UpdateProductModel.objects.filter(owner=request.user).delete()

                                            
                if response.status_code == 200:
                    messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + 'Product Catalog Updated!')
                    
                elif response.status_code == 400:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + 'Error in updating product!')
                    
                elif response.status_code == 409:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!3')
                    
                else:
                    messages.add_message(request, messages.ERROR, (response.text) + '!4')
                return redirect(to='catalogupdate')
            else:
                messages.add_message(request, messages.ERROR, 'Please Add/Activate your AppKey/SecretKey!')
                return redirect(to='catalogupdate')
    
    return render(request, 'product/catalogupdate.html', context)


@login_required
def catalogadd(request):
    context = {
        'form': UploadProductCatalogForm(),
        'nav_prod2_active': True
    }
    if request.method == 'POST':
        form = UploadProductCatalogForm(request.POST, request.FILES or None)
        if form.is_valid():
    
            appkey = form.cleaned_data['appkey']
            secretkey = form.cleaned_data['secretkey']
            products = form.cleaned_data['productcatalog']

            products_df = pd.read_csv(products)
            products_df = products_df.fillna({'Description': 'null'})
            products_df = products_df.fillna({'SKU': 'Null'})
            products_df = products_df.fillna({'Product Price': '0'})
            products_df['Product Price'] = products_df['Product Price'].astype(float)
            products_df.fillna('', inplace=True)

            for i, row in products_df.iterrows():

                AddProductModel.objects.create(
                    external_id=row[0],
                    product_title=row[1],
                    description=row[2],
                    product_url=row[3],
                    product_price=row[4],
                    sku=row[5],
                    processed = False,
                    owner=request.user,

                )
                print(row)

            
            utoken = getkey(request, appkey, secretkey)

            if utoken:
                data = AddProductModel.objects.filter(owner=request.user).filter(processed=False)
                serializer = AddProductModelSerializer(data, many=True)
                

                for i in serializer.data:

                    payload = {
                                "product": {
                                    "external_id": i['external_id'],
                                    "name": i['product_title'],
                                    "description": i['description'],
                                    "url": i['product_url'],
                                    "price": i['product_price'],
                                    "sku": i['sku']
                                }
                            }

                    headers = {
                        "X-Yotpo-Token": f"{utoken}",
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                        }
                    
                    url = f"https://api.yotpo.com/core/v3/stores/{appkey}/products"
                   

                    response = requests.request("POST", url=url, json=payload, headers=headers)
                    delete = AddProductModel.objects.filter(owner=request.user).delete()
                    

                                            
                if response.status_code == 201:
                    messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + 'Product Added to Catalog')
                    
                elif response.status_code == 400:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + 'Error in adding product!')
                    
                elif response.status_code == 409:
                    messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!3')
                    
                else:
                    messages.add_message(request, messages.ERROR, (response.text) + '!4')
                return redirect(to='catalogadd')
            else:
                messages.add_message(request, messages.ERROR, 'Please Add/Activate your AppKey/SecretKey!')
                return redirect(to='catalogadd')
    else:
        return render(request, 'product/catalogadd.html', context)

    return render(request, 'product/catalogadd.html', context)


@login_required
def viewproductbyid(request):
    return render(request, 'product/viewproductbyid.html')

    
