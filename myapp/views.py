from django.shortcuts import render,redirect
from myapp.models import users
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

    
# Create your views here.

def home(request):
    return render(request, "home.html")



def login_page(request):
    if request.method == "POST":
         if(
            request.POST.get("email")
            and request.POST.get("password")
        ):
            object= users()
            object.email = request.POST.get("email")
            object.password = request.POST.get("password")

        # Authenticate user
            #user = authenticate(request, email= object.email, password= object.password)
            if (users.objects.filter(email=object.email).exists() and users.objects.filter(password=object.password).exists()):
                return render(request, "home.html")

            else:
            # Authentication failed
                return redirect("error")
    else:
        return render(request, "login_page.html")

def signup_page(request):
    if request.method == "POST":
        if(
            request.POST.get("name")
            and request.POST.get("email")
            and request.POST.get("password")
            and request.POST.get("phone_no")
        ):

            object=users()
            object.name=request.POST.get('name')
            object.email=request.POST.get('email')
            object.password=request.POST.get('password')
            object.phone_no=request.POST.get('phone_no')
        

        # Check if the user with the given email already exists
            if users.objects.filter(email=object.email).exists():
            
                return render(request, "login_page.html")

        # If the user doesn't exist, create a new user
        new_user = users(name=object.name, email=object.email, password=object.password, phone_no=object.phone_no)
        new_user.save()

        return redirect("login_page")
    else:
        return render(request, "signup_page.html")
