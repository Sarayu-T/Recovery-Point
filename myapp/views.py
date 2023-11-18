from django.shortcuts import redirect, render
from myapp.models import LostItemDetails, FoundItemDetails, users
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages   
from django.template.loader import render_to_string



def home(request):
    return render(request, 'home.html')

def afterReport(request):
    return render(request, 'afterReport.html') 

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the user with the given email exists
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
            request.session['email'] = email

            # Check the hashed password
            if check_password(password, user.password):
                return render(request, "home.html")
            else:
                # Authentication failed
                messages.error(request, 'Invalid credentials. Please try again.')
                return redirect(reverse("login_page"))
        else:
            # User not found
            messages.error(request, 'User not found. Please sign up.')
            return redirect(reverse("login_page"))
    else:
        return render(request, "login_page.html")

def signup_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_no = request.POST.get("phone_no")

        # Hash the password
        hashed_password = make_password(password)

        # Check if the user with the given email already exists
        if users.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            request.session['email'] = email
            return render(request, "login_page.html")
        
        if users.objects.filter(phone_no=phone_no).exists():
            messages.error(request, 'User with this phone_no already exists.')
            return render(request, "login_page.html")

        # If the user doesn't exist, create a new user
        new_user = users(name=name, email=email, password=hashed_password, phone_no=phone_no)
        new_user.save()

        return redirect(reverse("login_page"))
    else:
        return render(request, "signup_page.html")

def report_lost_item(request):
    if request.method == 'POST':
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

            user_email = request.session['email']
            user = users.objects.get(email=user_email)
            item.user_id = user.user_id

            if 'item_image' in request.FILES:
                img = request.FILES['item_image']
                file_extension = img.name.split('.')[-1].lower()
                
                if file_extension in ['jpg', 'jpeg', 'png']:
                    item.item_image = img               
                else:  # Invalid image format
                    error = 1
                    messages.error(request, "Please upload only .png, .jpg, .jpeg format")
                    return render(request, 'alert.html', {'error': error})
            try:
                item.save()
                send_mail_report_lost(item, user_email)  # Sending copy of Item details
                return redirect('afterReport')
            except Exception as e:
                messages.error(request, f"Error saving report! {e}")      
        else:  # Required fields are missing
            return redirect('report_lost_item')
    else:  
        return render(request, 'report_lost_item.html', {'error_message': 'Item Details not recieved properly.'})

def report_found_item(request):
    if request.method == 'POST':
        print("SUBMITTED DATA:", request.POST)  # Print the submitted data
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

            user_email = request.session['email']
            user = users.objects.get(email=user_email)
            item.user_id = user.user_id

            if 'item_image' in request.FILES:
                img = request.FILES['item_image']
                file_extension = img.name.split('.')[-1].lower()
                
                if file_extension in ['jpg', 'jpeg', 'png']:
                    item.item_image = img              
                else:  # Invalid image format
                    error = 2
                    messages.error(request, "Please upload only .png, .jpg, .jpeg formats")
                    return render(request, 'alert.html', {'error': error})
            try: 
                item.save()
                send_mail_report_found(item, user_email)  # Sending copy of Item details
                return redirect('afterReport')
            except Exception as e:
                messages.error(request, f"Error saving item: {e}")
        else:  # Required fields are missing
            return redirect('report_found_item')
    else:   
        return render(request, 'report_found_item.html')
    
def send_mail_report_lost(item, email):
    subject = 'Lost and Found System: Lost Item Report'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    item_dict = {
        'item_name': item.item_name,
        'category': item.category,
        'description': item.description,
        'location_lost': item.location_lost,
        'item_image': item.item_image.url if item.item_image else "Image not available",  
        'datetime': item.datetime,
    }

    context = {'item': item_dict}
    email_message = render_to_string('reportEmail_lost.html', context)
    send_mail(subject, '', from_email, recipient_list, html_message=email_message) 

def send_mail_report_found(item, email):
    subject = 'Lost and Found System: Found Item Report'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    item_dict = {
        'item_name': item.item_name,
        'category': item.category,
        'description': item.description,
        'location_lost': item.location_found,
        'item_image': item.item_image.url if item.item_image else "Image not available",  
        'datetime': item.datetime,
    }

    context = {'item': item_dict}
    email_message = render_to_string('reportEmail_found.html', context)
    send_mail(subject, '', from_email, recipient_list, html_message=email_message) 

