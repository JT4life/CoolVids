from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def register(request):
    if request.method == "POST":
    # check and verify the password1 and password2
        first_name = request.POST['first_name'] #getting name from register1.html form
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists(): #check if existing usernames
                print("User already exists")
                messages.info(request,'Username already exists')
            else:
                user = User.objects.create_user(first_name=first_name, username=username, password=password1, last_name=last_name,
                                                email=email)
                user.save()
                print("User created")
                return redirect('login')
        else:
            messages.info(request, "Passwords did not match")
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        user = auth.authenticate(username=username,password=password1)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Invalid User Please Try Again')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')