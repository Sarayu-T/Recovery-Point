from django.shortcuts import render,redirect
from .models import Ticket
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    return render(request, 'home.html')

def send_email_view(request):
    
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
        recipient_list=['sarayuthampan@gmail.com'],
        html_message=email_message,
    )
    return redirect('afterTicket')

def ticket(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        issue = request.POST['issue']

        # Create a new Ticket object and save it to the database
        Ticket.objects.create(name=name, subject=subject, issue=issue)
        send_email_view(request)
        return redirect('afterTicket')
    else:
        return render(request, 'ticket.html')




def afterTicket(request):
    return render(request, 'afterTicket.html')

def afterReport(request):
    return render(request, 'afterReport.html')