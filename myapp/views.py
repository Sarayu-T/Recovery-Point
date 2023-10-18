from django.shortcuts import redirect, render
from myapp.models import LostItemDetails, FoundItemDetails
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def afterReport(request):
    return render(request, 'afterReport.html') 

def report_lost_item(request):
    if request.method == 'POST':
        print("Received POST request")  # Check if the view is getting the POST request

        print(request.POST)  # Print the submitted data
        if request.POST.get('item_name') and request.POST.get('category') and request.POST.get('description'):

            item = LostItemDetails()

            item.item_name = request.POST.get('item_name')
            item.category = request.POST.get('category')
            item.description = request.POST.get('description')
            item.location_lost = request.POST.get('location_lost')

            if request.POST.get('datetime'):
                item.datetime = request.POST.get('datetime')
            else:
                item.datetime = timezone.now()  # Set current datetime if none is provided

            if len(request.FILES) != 0:
                item.item_image = request.FILES['item_image']
        
            try:
                item.save()
            except Exception as e:
                print("Error saving item:", e)
                #messages.error(request, "Error saving item: {}".format(e))
            return redirect('afterReport')
        else:
            print("Missing required fields")  # Check if any required fields are missing
            return redirect('report_lost_item')
    else:  
        return render(request, 'report_lost_item.html')
    

def report_found_item(request):
    if request.method == 'POST':
        print("Received POST request")  # Check if the view is getting the POST request

        print(request.POST)  # Print the submitted data
        if request.POST.get('item_name') and request.POST.get('category') and request.POST.get('description'):

            item = FoundItemDetails()

            item.item_name = request.POST.get('item_name')
            item.category = request.POST.get('category')
            item.description = request.POST.get('description')
            item.location_lost = request.POST.get('location_found')

            if request.POST.get('datetime'):
                item.datetime = request.POST.get('datetime')
            else:
                item.datetime = timezone.now()  # Set current datetime if none is provided

            if len(request.FILES) != 0:
                item.item_image = request.FILES['item_image']
        
            try:
                item.save()
            except Exception as e:
                print("Error saving item:", e)
                #messages.error(request, "Error saving item: {}".format(e))
            return redirect('afterReport')
        else:
            print("Missing required fields")  # Check if any required fields are missing
            return redirect('report_found_item')
    else:  
        return render(request, 'report_found_item.html')