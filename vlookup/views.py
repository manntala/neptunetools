from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import csv

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from .models import CatalogModel, ReviewsModel, UploadedCSVModel
from .forms import UploadDataForm, UploadScraperForm
import uuid

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


fs = FileSystemStorage(location='tmp/')
pc = uuid.uuid4()


@login_required
def uploadcatalog(request):
    if request.method == 'POST':
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
        
        catalog_list = []
        for id_, row in enumerate(reader):
            (
                product_id,
                product_name,
                product_url,
                product_image_url,
                product_price,
                currency,
                spec_upc,
                spec_mpn,
                spec_brand,
                spec_isbn,
                spec_sku,
                product_tags,
                blaclisted,
                product_group,
            ) = row
            catalog_list.append(
                CatalogModel(
                    product_id=product_id,
                    product_name=product_name,
                    product_url=product_url,
                    product_image_url=product_image_url,
                    product_price=product_price,
                    currency=currency,
                    spec_upc=spec_upc,
                    spec_mpn=spec_mpn,
                    spec_brand=spec_brand,
                    spec_isbn=spec_isbn,
                    spec_sku=spec_sku,
                    product_tags=product_tags,
                    blacklisted=blaclisted,
                    product_group=product_group,
                    owner=request.user,
                    pc = pc,
                    processed=False,
             )
            )

        CatalogModel.objects.bulk_create(catalog_list)
        messages.success(request, 'Product Catalog uploaded!')
        return redirect(to='/uploadcatalog#uploadcatalog')
        # return render(request, 'vlookup/uploadcatalog.html')

    
    return render(request, "vlookup/uploadcatalog.html")

@login_required
def uploadreviews(request):
    if request.method == 'POST':
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
        
        review_list = []
        for id_, row in enumerate(reader):
            (
                review_id,
                app_key,
                published,
                review_title,
                review_content,
                review_score,
                date,
                user_type,
                sku,
                product_url,
                product_title,
                product_description,
                product_image_url,
                display_name,
                email,
                md_customer_country,
                comment_content,
                comment_published,
                comment_created,
                review_image,
                title,
                sub_title,
                int_value,
                string_value,


            ) = row
            review_list.append(
                ReviewsModel(
                    review_id=review_id,
                    app_key=app_key,
                    published=published,
                    review_title=review_title,
                    review_content=review_content,
                    review_score=review_score,
                    date=date,
                    user_type=user_type,
                    sku=sku,
                    product_url=product_url,
                    product_title=product_title,
                    product_description=product_description,
                    product_image_url=product_image_url,
                    display_name=display_name,
                    email=email,
                    md_customer_country=md_customer_country,
                    comment_content=comment_content,
                    comment_published=comment_published,
                    comment_created=comment_created,
                    review_image=review_image,
                    title=title,
                    sub_title=sub_title,
                    int_value=int_value,
                    string_value=string_value,
                    owner=request.user,
                    pc = pc,
                    processed=False,
             )
            )

        ReviewsModel.objects.bulk_create(review_list)
        messages.success(request, 'Import File uploaded!')
        return redirect(to='/uploadcatalog#uploadcatalog')
        # return render(request, 'vlookup/uploadcatalog.html')

    
    return render(request, "vlookup/uploadcatalog.html")

@login_required
def vlookup(request):
    if request.method == 'POST':
        catalog = request.FILES['catalog']
        reviews = request.FILES['reviews']

        # read csv files
        catalog_df = pd.read_csv(catalog)
        reviews_df = pd.read_csv(reviews)

        # if catalog_df is in review_df
        # if reviews_df is in catalog_df

        for i, row in reviews_df.iterrows():
            product_title = row[10]
            row_number = i
            for x, row in catalog_df.iterrows():
                if row[1] == product_title: 
                    reviews_df.at[row_number, 'product_id'] = row[0]
                    reviews_df.at[row_number, 'product_url'] = row[2]
                    reviews_df.at[row_number, 'product_image_url'] = row[3]
        
        tmp_name = str(uuid.uuid4())
        file_path = 'static/tmp/'+tmp_name+'/'
        file_path = makedirs(file_path)
        reviews_df.to_csv(file_path+'reviews_processed.csv', index=False)
        
        context = {
            'file_path': file_path+'reviews_processed.csv',
            'file_name': 'reviews_processed.csv',
        }
        messages.add_message(request, messages.SUCCESS, 'Processing done!')
        return render(request, 'vlookup/vlookup.html', context)
        # return render(request, "vlookup/vlookup.html", context)
    
    else:
        return render(request, "vlookup/vlookup.html")

@login_required
def view_products(request):
    
    return redirect(view_products(request))

@login_required
def autoretrieve(request):
    form =  UploadDataForm()
    context = {
    'form' : form
    }

    if request.method == 'POST':
        data_form = UploadDataForm(request.POST, request.FILES or None)
        
        if data_form.is_valid():

            catalog = data_form.cleaned_data['catalog']
            reviews = data_form.cleaned_data['reviews']

            # read csv files
            catalog_df = pd.read_csv(catalog)
            reviews_df = pd.read_csv(reviews)

            # if catalog_df is in review_df
            # if reviews_df is in catalog_df

            for i, row in reviews_df.iterrows():

                try :
                    product_title = row[10]
                    row_number = i
                    for x, row in catalog_df.iterrows():
                        if row[1] == product_title: 
                            reviews_df.at[row_number, 'product_id'] = row[0]
                            reviews_df.at[row_number, 'product_url'] = row[2]
                            reviews_df.at[row_number, 'product_image_url'] = row[3]
                except:
                    messages.add_message(request, messages.ERROR, 'Product Title not found!')
                    return render(request, "vlookup/autoretrieve.html", context)    

                # product_title = row[10]
                # row_number = i
                # for x, row in catalog_df.iterrows():
                #     if row[1] == product_title: 
                #         reviews_df.at[row_number, 'product_id'] = row[0]
                #         reviews_df.at[row_number, 'product_url'] = row[2]
                #         reviews_df.at[row_number, 'product_image_url'] = row[3]
            
            tmp_name = str(uuid.uuid4())
            file_path = 'static/tmp/'+tmp_name+'/'
            file_path = makedirs(file_path)
            reviews_df.to_csv(file_path+'reviews_processed.csv', index=False)
            
            context = {
                'file_path': file_path+'reviews_processed.csv',
                'file_name': 'reviews_processed.csv',
                'form' : form
            }
            messages.add_message(request, messages.SUCCESS, 'Processing done!')
            return render(request, 'vlookup/autoretrieve.html', context)
            # return render(request, "vlookup/vlookup.html", context)

        messages.add_message(request, messages.ERROR, 'Invalid File/s!')
        return render(request, "vlookup/autoretrieve.html", context)

    else:
        return render(request, "vlookup/autoretrieve.html", context)

    return render(request, "vlookup/autoretrieve.html", context)

@login_required
def resetform(request):
    form =  UploadDataForm()
    context = {
    'form' : form
    }
    return render(request, "vlookup/vlookup.html", context)

@login_required
def resetscraperform(request):
    form =  UploadScraperForm()
    context = {
    'form' : form
    }
    return render(request, "vlookup/shopifyscraper.html", context)

@login_required
def shopifyscraper(request):
    form =  UploadScraperForm()
    context = {
    'form' : form
    }
    # url = 'https://www.biggerthehoop.com/products.json'

    if request.method == 'POST':
        data_form = UploadScraperForm(request.POST, request.FILES or None)

        if data_form.is_valid():

                shopifyurl = data_form.cleaned_data['shopifyurl'] + '/products.json'
                reviews = data_form.cleaned_data['reviews']

                # print(shopifyurl)

                # read csv files
                
                reviews_df = pd.read_csv(reviews)

                try :
                    response = requests.get(shopifyurl)
                    data = response.json()
                    # print(data)
                except :
                    messages.add_message(request, messages.ERROR, 'Invalid Shopify URL!')
                    return render(request, "vlookup/shopifyscraper.html", context)
 

                product_list = []
                for item in data['products']:
                    
                    product_id = item['id']
                    product_title = item['title']
                   

                    products = {
                        'product_id': product_id,
                        'product_title': product_title,
                        
                    }
                    product_list.append(products)

                url_df = pd.DataFrame(product_list, columns=['product_id', 'product_title'])
                # url_df.to_csv('static/tmp/products.csv', index=False)
                # print('done')

                for i, row in reviews_df.iterrows():
                    product_title = row[10]

                    row_number = i
                    for x, row in url_df.iterrows():
                        
                        if row[1] == product_title: 
                            reviews_df.at[row_number, 'product_id'] = row[0]
                            
                
                tmp_name = str(uuid.uuid4())
                file_path = 'static/tmp/'+tmp_name+'/'
                file_path = makedirs(file_path)
                reviews_df.to_csv(file_path+'reviews_processed.csv', index=False)
                
                context = {
                    'file_path': file_path+'reviews_processed.csv',
                    'file_name': 'reviews_processed.csv',
                    'form' : UploadScraperForm()
                }
                messages.add_message(request, messages.SUCCESS, 'Processing done!')
                return render(request, 'vlookup/shopifyscraper.html', context)
            

    else:
        return render(request, "vlookup/shopifyscraper.html", context)

    return render(request, "vlookup/shopifyscraper.html", context)