from django.contrib import admin
from .models import UpdateProductModel

class UpdateProductModelAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'product_title', 'product_url', 'product_image_url', 'blacklisted', 'product_group', 'owner', 'processed',)
    readonly_fields = ('external_id', 'owner',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UpdateProductModel, UpdateProductModelAdmin)
