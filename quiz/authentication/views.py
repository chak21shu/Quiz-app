from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']  
        if password == confirmpassword:
            if not User.objects.filter(username = username).exists():
                user = User.objects.create(username = username,password = password,email = email)
                user.set_password(password)
                user.save()
                messages.success(request, 'User created sucessfully')
                login(request,user)
                return redirect('dashboard')
                
            else:
                messages.error(request,"username alraedy exists")
                return redirect('signup')


        else:
            
            messages.error(request,'password do not match')  
            return redirect('signup')       
    return render(request,'signup.html')
    


def login_view(request):
        user = request.user
        if user.is_authenticated:
            return redirect('dashboard')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is None:
                return redirect('login')
            login(request, user)
            return redirect('dashboard')
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')  


