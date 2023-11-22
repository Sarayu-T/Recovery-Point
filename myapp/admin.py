from django.contrib import admin
from myapp.models import LostItemDetails, FoundItemDetails, users, Ticket

# Register your models here.
admin.site.register(users)
admin.site.register(LostItemDetails)
admin.site.register(FoundItemDetails)
admin.site.register(Ticket)
