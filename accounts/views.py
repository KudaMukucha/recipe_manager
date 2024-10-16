from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import RegisterChefForm

# Create your views here.
User = get_user_model()

def register_chef(request):
    h2 = 'Register'
    user = None
    if request.method == 'POST':
        form = RegisterChefForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_chef = True
            user.username = user.email
            user.save()
            messages.success(request,'Account created successfully. Please login')
            return redirect('accounts:login')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again.')
            return redirect('accounts:register-chef')
    else:
        form = RegisterChefForm()
        return render(request,'accounts/register-chef.html',{'form':form,'h2':h2})

def login_user(request):
    h2 = 'Login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None and user.is_active:
            login(request,user)
            return redirect('website:home')
        else:
            messages.warning(request,'Oops, something went wrong. Please check form errors')
            return render(request,'accounts/login.html',{'username':username})
    else:
        return render(request,'accounts/login.html',{'h2':h2})

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect('website:home')

