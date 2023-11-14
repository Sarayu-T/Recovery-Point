from django.shortcuts import redirect, render
from myapp.models import LostItemDetails, FoundItemDetails, users
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def afterReport(request):
    return render(request, 'afterReport.html') 

def report_lost_item(request):
    if request.method == 'POST':
        print("Received POST request")  # Check if the view is getting the POST request
        print("SUBMITTED DATA:", request.POST)  # Print the submitted data
        if (
            request.POST.get('item_name') 
            and request.POST.get('category') 
            and request.POST.get('description') 
            and request.POST.get('location_lost')
        ):
            item = LostItemDetails()
            item.item_name = request.POST.get('item_name')
            item.category = request.POST.get('category')
            item.description = request.POST.get('description')
            item.location_lost = request.POST.get('location_lost')

            if request.POST.get('datetime'):
                item.datetime = request.POST.get('datetime')
            else:
                item.datetime = timezone.now()  # Set current datetime if none is provided

            if 'item_image' in request.FILES:
                img = request.FILES['item_image']
                file_extension = img.name.split('.')[-1].lower()
                
                if file_extension in ['jpg', 'jpeg', 'png']:
                    try:
                        item.item_image = img               
                    except Exception as e:
                        return HttpResponse(f"Invalid image: {e}")
                
                else:
                    error = 1
                    return render(request, 'alert.html', {'error': error})
            try:
                item.save()
                return redirect('afterReport')
            except Exception as e:
                return HttpResponse(f"Error saving item: {e}")       
        else:
            print("Missing required fields")  # Check if any required fields are missing
            return redirect('report_lost_item')
    else:  
        return render(request, 'report_lost_item.html', {'error_message': 'Item Details not recieved properly.'})

def report_found_item(request):
    if request.method == 'POST':
        print("Received POST request")  # Check if the view is getting the POST request
        print("Submissted data:", request.POST)  # Print the submitted data
        if (
            request.POST.get('item_name') 
            and request.POST.get('category') 
            and request.POST.get('description') 
            and request.POST.get('location_found')
        ):
            item = FoundItemDetails()
            item.item_name = request.POST.get('item_name')
            item.category = request.POST.get('category')
            item.description = request.POST.get('description')
            item.location_found = request.POST.get('location_found')

            if request.POST.get('datetime'):
                item.datetime = request.POST.get('datetime')

            if 'item_image' in request.FILES:
                img = request.FILES['item_image']
                file_extension = img.name.split('.')[-1].lower()
                
                if file_extension in ['jpg', 'jpeg', 'png']:
                    try:
                        item.item_image = img              
                    except Exception as e:
                        return HttpResponse(f"Invalid image: {e}")
                else:
                    error = 2
                    return render(request, 'alert.html', {'error': error})
            try:
                item.save()
                return redirect('afterReport')
            except Exception as e:
                return HttpResponse(f"Error saving item: {e}")
        else:
            print("Missing required fields")  # Check if any required fields are missing
            return redirect('report_found_item')
    else:   
        return render(request, 'report_found_item.html', {'error_message': 'Item Details not recieved properly.'})
    

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

