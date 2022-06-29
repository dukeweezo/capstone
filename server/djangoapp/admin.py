from django.contrib import admin
from .models import CarModel, CarMake

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'dealer_id', 'name', 'car_type', 'year']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
