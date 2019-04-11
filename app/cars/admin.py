from django.contrib import admin
from . import models


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'name',
        'car_count',
    )


@admin.register(models.Kind)
class KindAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'name',
        'car_count',
    )


@admin.register(models.Model)
class ModelAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'name',
        'car_count',
    )

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'status',
        'auction_start_time',
        'auction_end_time',
        'owner',
        'model',
    )
    
    list_filter = (
        'status',
        'owner',
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
        'represent',
    )
