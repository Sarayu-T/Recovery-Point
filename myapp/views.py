from django.shortcuts import render,redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from myapp.models import LostItemDetails, FoundItemDetails, users, Ticket, admin
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages   
from django.template.loader import render_to_string
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.shortcuts import render, redirect
from django.http import JsonResponse


# Create your views here.

def home(request):
    return render(request, 'home.html')

def afterTicket(request):
    return render(request, 'afterTicket.html')

def afterReport(request):
    return render(request, 'afterReport.html')  

def initial_page(request):
    return render(request, 'initial_page.html')  

#    USER FUNCTIONS

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
            messages.error(request, 'User with this phone number already exists.')
            return render(request, "login_page.html")

        # If the user doesn't exist, create a new user
        new_user = users(name=name, email=email, password=hashed_password, phone_no=phone_no)
        new_user.save()

        return redirect(reverse("login_page"))
    else:
        return render(request, "signup_page.html")
    
def send_email_view(request, email):  
    form_data = {
        'name': request.POST.get('name'),
        'subject': request.POST.get('subject'),
        'issue': request.POST.get('issue'),
    }
    email_message = render_to_string('ticketEmail.html', form_data)

    # Send the email
    send_mail(
        subject='Your Ticket Details',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=email_message,
    )
    return redirect('afterTicket')

def ticket(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        issue = request.POST['issue']                    
        user_email = request.session['email']
        user = users.objects.get(email=user_email)

        Ticket.objects.create(name=name, subject=subject, issue=issue,user_id=user.user_id)
        
        send_email_view(request, user_email)
        return redirect('afterTicket')
    else:
        return render(request, 'ticket.html')

def search_items(request):
    query = request.GET.get('q')
    filter_by = request.GET.get('filter_by')

    if query and filter_by in ['item_name', 'category', 'description']:
        filter_condition = {f'{filter_by}__icontains': query}

        if filter_by == 'item_name':
            lost_items = LostItemDetails.objects.filter(item_name__icontains=query)
            found_items = FoundItemDetails.objects.filter(item_name__icontains=query)
        elif filter_by == 'category':
            lost_items = LostItemDetails.objects.filter(category__icontains=query)
            found_items = FoundItemDetails.objects.filter(category__icontains=query)
        elif filter_by == 'description':
            lost_items = LostItemDetails.objects.filter(description__icontains=query)
            found_items = FoundItemDetails.objects.filter(description__icontains=query)
    else:
        lost_items = LostItemDetails.objects.none()
        found_items = FoundItemDetails.objects.none()

    return render(request, 'search_results.html', {'lost_items': lost_items, 'found_items': found_items})

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
        return render(request, 'report_lost_item.html')
                    
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

def view_reports(request):
    user_email = request.session.get('email')
    user = users.objects.get(email=user_email)
    user_reports_lost = LostItemDetails.objects.filter(user_id=user.user_id)   
    user_reports_found = FoundItemDetails.objects.filter(user_id=user.user_id)    
    return render(request, 'view_reports.html', {'user_reports_lost': user_reports_lost, 'user_reports_found': user_reports_found})

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
        'location_found': item.location_found,
        'item_image': item.item_image.url if item.item_image else "Image not available",  
        'datetime': item.datetime,
    }

    context = {'item': item_dict}
    email_message = render_to_string('reportEmail_found.html', context)
    send_mail(subject, '', from_email, recipient_list, html_message=email_message) 

def matching_algorithm(description1, description2):
    # Use fuzzy string matching to calculate a similarity score
    similarity_score = fuzz.partial_ratio(description1, description2)
    return similarity_score

def model_matching(request):
    user_email = request.session['email']
    user = users.objects.get(email=user_email)
    lost_items = LostItemDetails.objects.filter(user_id= user.user_id)

    matched_items = []

    for lost_item in lost_items:
        matching_found_items = FoundItemDetails.objects.filter(Q(category=lost_item.category))

        # Filter based on the description similarity using the matching algorithm
        for found_item in matching_found_items:
            similarity_desc = matching_algorithm(lost_item.description, found_item.description)
            similarity_name = matching_algorithm(lost_item.item_name, found_item.item_name)
            similarity_loc = matching_algorithm(lost_item.location_lost, found_item.location_found)
            
            if (similarity_desc > 20 and similarity_name > 70 and similarity_loc > 45):  # Adjust the threshold as needed
                matched_items.append((lost_item, found_item))

    return render(request, 'model_matching.html', {'matched_items': matched_items})


#    ADMIN ROLES 

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'lostandfoundsystem13@gmail.com' and password == 'admin123':       
            return redirect('admin_user')
        else:
            return redirect('admin_login')        

    return render(request, 'admin_login.html')

def admin_user(request):
    user = users.objects.all() # getting all users
    return render(request, 'admin_user.html', {'users': user})

def admin_lost_item(request):
    lost_items = LostItemDetails.objects.all()
    return render(request, 'admin_lost_item.html', {'lost_items': lost_items})

def admin_found_item(request):
    found_items = FoundItemDetails.objects.all()
    return render(request, 'admin_found_item.html', {'found_items': found_items})

def admin_ticket(request):
    tickets = Ticket.objects.all() # getting all tickets
    return render(request, 'admin_ticket.html', {'tickets': tickets})

def delete_user(request, user_id):
    user = get_object_or_404(users, user_id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_user')

def delete_lost_item(request, id):
    lost_item = get_object_or_404(LostItemDetails, id=id)
    if request.method == 'POST':
        lost_item.delete()
    return redirect('admin_lost_item')

def delete_found_item(request, id):
    found_item = get_object_or_404(FoundItemDetails, id=id)
    if request.method == 'POST':
        found_item.delete()
    return redirect('admin_found_item')

def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
    return redirect('admin_ticket')
