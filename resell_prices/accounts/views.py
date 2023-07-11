from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from django.contrib import auth

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Account,UserProfile
from .forms import UserProfileForm,UserForm

from .forms import RegistrationForm


# varification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,"Account Created Successfully!!")
            return redirect('account:login')
            
    else:
        form = RegistrationForm()
    context ={
        'form':form,
    }
    return render(request,'account/signup.html',context)


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('account:display_profile'))
        else:
            messages.error(request,'Invalid login User')
            return redirect('account:login')
    context ={
        'form':form,
    }
    
    return render(request,'account/login.html',context)

    
        


@login_required(login_url='account:login')
def user_profile(request):
    
    profile = UserProfile.objects.get(user=request.user)
    
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
       
        form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            
            messages.success(request,"Profile Updated Successfully !!!")
            form = UserProfileForm(instance=profile)
    return render(request,'account/change_profile.html',context={'form':form})


@login_required(login_url='account:login')
def profile(request):
    
    return render(request,'account/profile.html')



@login_required(login_url='account:login')
def logout_user(request):
    logout(request)
    messages.warning(request,'You are Logged out')
    return HttpResponseRedirect(reverse('account:login'))