from django.contrib import admin
from myapp.models import Item
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
  list_display = ('item_name', 'description', 'location_lost', 'date_reported')
  list_filter = ('item_name', 'location_lost')
  search_fields = ('item_name', 'description', 'location_lost')
