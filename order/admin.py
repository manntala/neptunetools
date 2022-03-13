from django.contrib import admin
from .models import OrderProcessModel, Csv, Post, OrderTemplate, GetKey

class OrderProcessModelAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'external_id', 'email', 'first_name', 'last_name', 'quantity', 'product_id', 'owner', 'sent',)
    readonly_fields = ('id', 'owner',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class GetKeyAdmin(admin.ModelAdmin):
    list_display = ('appkey', 'secretkey', 'token', 'owner', 'active',)
    readonly_fields = ('id', 'owner', 'token',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(OrderProcessModel, OrderProcessModelAdmin)
admin.site.register(Csv)
admin.site.register(Post)
admin.site.register(OrderTemplate) 
admin.site.register(GetKey, GetKeyAdmin)