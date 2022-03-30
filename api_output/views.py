from django.shortcuts import render, redirect
import requests
import random
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import datetime

from .forms import BuyForm
from order.forms import GetKeyForm

def symbol_remove(string):
    replaced = string.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('"', '').replace('\'', '').replace(':', ' ').replace(',', '').replace('errors', '').replace('error', '').replace('message', '')
    return replaced.title()

random_list = [1,2,3,4,5,6,7,8]
random_pic = [1,2,3,4,5,6,7,8]


def api_reviews(request):

    url = "https://api.yotpo.com/v1/apps/pX24FKZoDxZliIxSRQQyJJpC4RFUyRNePwdgWzv5/reviews?utoken=FvB52lhkqJqk4OV9oGYaXdztGChNsYX58dNTjbsZ&count=7"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers)
    reviews = response.json()['reviews']

    context = {
        'nav_api_reviews1' : True,
        'reviews' : reviews,
        'random_list' : random.sample(random_list, 8),
        'random_pic' : random.sample(random_pic, 8),
    }
   
    return render(request, 'api_output/reviews.html', context)

def api_reviews2(request):
    return render(request, 'api_output/reviews2.html')


def submit_review(request):
    url = request.META.get('HTTP_REFERER')
    email = request.POST.get('email')
    if request.method == 'POST': 
        try: 
            obj = ReviewRating.objects.filter(email=email).exists()
            if obj:
                reviews = ReviewRating.objects.get(email=email)
                form = ReviewForm(request.POST, instance=reviews)
                form.save()       
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url) 
            else:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    data = ReviewRating()
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.email = form.cleaned_data['email']
                    
                    data.save()
                    messages.success(request, 'Thank you! Your review has been added.')
                    return redirect(url) 
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.email = form.cleaned_data['email']
                
                data.save()
                messages.success(request, 'Thank you! Your review has been added.')
                return redirect(url)
                      
    context = {
        'nav_api_reviews2' : True,
    }
    return render(request, 'api_output/submit_review.html', context)


def reviewAPI(request):
    if request.method == 'POST': 
       
        email = request.POST.get('email')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        review = request.POST.get('review')
        rating = int(request.POST.get('rating'))

        print(rating)


        url = "https://api.yotpo.com/v1/widget/reviews"

        payload = {
            "appkey": "pX24FKZoDxZliIxSRQQyJJpC4RFUyRNePwdgWzv5",
            "domain": "https://laptopmio.myshopify.com",
            "sku": "5922652225690",
            "product_title": "MSI GE66 10SFS-072 Raider Laptop",
            "product_description": "Gaming Laptop",
            "product_url": "https://laptopmio.myshopify.com/products/msi-ge66-10sfs-072-raider",
            "product_image_url": "https://cdn.shopify.com/s/files/1/0510/7056/6554/products/MsiGE66-3_600x.jpg?v=1605271531",
            "display_name": name,
            "email": email,
            "is_incentivized": True,
            "review_content": review,
            "review_title": subject,
            "review_score": rating
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

        return redirect('/api_output/submit_review')
    
    return render(request, 'api_output/submit_review.html')

@login_required
def buy(request):
    form = BuyForm()


    context = {
        'form': form,

    }
    # order_processes = get_list_or_404(OrderProcessModel)
    # serializer = OrderProcessSerializer(order_processes, many=True)

    if request.method == 'POST':
        

        order_external_id = request.POST.get('order_external_id')
        order_date = '2022-03-24'
        cs_email = 'magnezyle@yahoo.com'
        first_name = 'Manny'
        last_name = 'Talaroc'
        quantity = 1
        product_id = 5922703704218




        payload = {
        "client_id": 'pX24FKZoDxZliIxSRQQyJJpC4RFUyRNePwdgWzv5',
        "client_secret": 'v5sP0XXNlY2GmcGH8GKncz91C3A4LZTqkgW3RaRg',
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
                            
            payload = { "order": {
                        "external_id": order_external_id,
                        "order_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "customer": {
                            "external_id": '1111',
                            "email": 'nameemail@email.com',
                            "first_name": 'Manny',
                            "last_name": 'Talaroc'
                        },
                        "line_items": [
                            {
                                "quantity": 1,
                                "external_product_id": 5922703704218
                            }
                        ],
                        "fulfillments": [
                        {
                            "fulfillment_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "external_id": order_external_id,
                            "status": "success",
                            "fulfilled_items": [
                                {
                                    "external_product_id": 5922703704218,
                                    "quantity": 1
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
            
            url = f"https://api.yotpo.com/core/v3/stores/pX24FKZoDxZliIxSRQQyJJpC4RFUyRNePwdgWzv5/orders"

            response = requests.request("POST", url=url, json=payload, headers=headers)
            print(response.text)

                

                
            if response.status_code == 201:
                messages.add_message(request, messages.SUCCESS, symbol_remove(response.text) + '!')   
                return redirect(to='buy') 
                delete = OrderProcessModel.objects.filter(owner=request.user).delete()
            elif response.status_code == 400:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')  
                return redirect(to='buy')  
                delete = OrderProcessModel.objects.filter(owner=request.user).delete()
            elif response.status_code == 409:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')   
                return redirect(to='buy') 
                delete = OrderProcessModel.objects.filter(owner=request.user).delete()
            else:
                messages.add_message(request, messages.ERROR, symbol_remove(response.text) + '!')
                return redirect(to='buy')
                delete = OrderProcessModel.objects.filter(owner=request.user).delete()
                  
                    
                     
                # else:
                #     messages.add_message(request, messages.ERROR, 'Invalid CSV!')
                #     return redirect(to='send')

        else:
            messages.add_message(request, messages.ERROR, 'Please Add/Activate your AppKey/SecretKey!')
            return redirect(to='buy')

    
   
    # end of post
    else:      
        return render(request, 'api_output/buy.html', context)