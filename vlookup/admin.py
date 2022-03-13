from django.contrib import admin
from .models import CatalogModel, ReviewsModel

class CatalogModelAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'owner', 'pc', 'processed',)
    readonly_fields = ('product_id', 'owner',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ReviewsModelAdmin(admin.ModelAdmin):
    list_display = ('sku', 'review_id', 'product_title', 'owner', 'pc', 'processed',)
    readonly_fields = ('sku', 'owner',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CatalogModel, CatalogModelAdmin)
admin.site.register(ReviewsModel, ReviewsModelAdmin)