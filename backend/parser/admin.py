from django.contrib import admin
from .models import Change_rate, Days_change_rate, Country, Covid_info


@admin.register(Change_rate)
class Change_ratesAdmin(admin.ModelAdmin):
    pass


@admin.register(Days_change_rate)
class Days_change_ratesAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Covid_info)
class Covid_infoAdmin(admin.ModelAdmin):
    search_fields = ('country__country', )