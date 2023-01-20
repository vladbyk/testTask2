from django.urls import path
from .views import country_view, change_rate_view, \
    covid_info_view, days_change_rate_view, plot_view, countries_view, rates_view, plot_rates_view

urlpatterns = [
    path('country/<int:pk>', country_view),
    path('change-rate/<int:pk>', change_rate_view),
    path('days-change-rate/<int:pk>', days_change_rate_view),
    path('covid-info/<int:pk>', covid_info_view),
    path('plot/', plot_view),
    path('countres/', countries_view),
    path('rates/', rates_view),
    path('change-rates/<str:rate>', plot_rates_view)
]
