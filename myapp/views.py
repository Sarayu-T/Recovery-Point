from django.shortcuts import redirect, render
from myapp.models import LostItemDetails, FoundItemDetails
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
        print("Submissted data:", request.POST)  # Print the submitted data
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
                    error_message = 'Please upload only image files.'
                    return render(request, 'report_lost_item.html', {'error_message': error_message})
            try:
                item.save()
                messages.success(request, "Your report has been submitted!")
                return redirect('afterReport')
            except Exception as e:
                messages.error(request, f"Error saving item: {e}")
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
            item.location_lost = request.POST.get('location_found')

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
                    error_message = 'Please upload only image files.'
                    return render(request, 'report_found_item.html', {'error_message': error_message})
            try:
                item.save()
                messages.success(request, "Your report has been submitted!")
                return redirect('afterReport')
            except Exception as e:
                messages.error(request, f"Error saving item: {e}")
                return HttpResponse(f"Error saving item: {e}")
        else:
            print("Missing required fields")  # Check if any required fields are missing
            return redirect('report_found_item')
    else:   
        return render(request, 'report_found_item.html', {'error_message': 'Item Details not recieved properly.'})