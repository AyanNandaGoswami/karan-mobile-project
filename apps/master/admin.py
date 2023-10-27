# django
from django.contrib import admin

# local import
from .models import *


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    search_fields = ('name', )


@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pin_no', 'dist')
    search_fields = ('name', )


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post_office')
    search_fields = ('name', )


admin.site.register(Finance)
