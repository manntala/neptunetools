from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfileUpdateForm
from account.models import Profile

get_default_profile_image = lambda: 'https://www.onlinewebfonts.com/icon/405142'

def registration_view(request):

    if request.user.is_authenticated: 
        return redirect(to='dashboard')
    
    context = {
        'form': RegistrationForm(request.POST)
    }
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            # login(request, account)
            # return redirect(dashboard)

            messages.add_message(request, messages.SUCCESS, 'Registration successful')
            return redirect('login')

        else:
            messages.add_message(request, messages.ERROR, 'Invalid registration')
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('dashboard')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(to='dashboard')

    form = AccountAuthenticationForm()
    context = {
        'form': form
    }

    # user = request.user
    # if user.is_authenticated:
    #     return redirect(account_view)
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)      
                return redirect('dashboard')
            
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            form = AccountAuthenticationForm()
            return redirect('login')
    else:
        form = AccountAuthenticationForm()


    context['login_form'] = form
    return render(request, 'account/index.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
         form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
            }
         )
    context['account_form'] = form
    return render(request, 'account/account.html', context)

@login_required
def update_view(request):
    u_form = AccountUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        u_form = AccountUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('update')

    else:
        u_form = AccountUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'nav_profile1': True
    }
    return render(request, 'account/update.html', context)

