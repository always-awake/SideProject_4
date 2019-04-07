from django.contrib import admin
from . import models


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'status',
        'auction_start_time',
        'owner',
        'brand',
        'kind',
        'model',
    )
    
    list_filter = (
        'status',
        'owner',
        'brand',
        'kind',
        'model',
    )

    list_display_links = (
        'id',
    )

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'car',
    )