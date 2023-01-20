from django.core.management import BaseCommand
import requests
from parser.models import Country, Covid_info, Days_change_rate


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_request()
        for day in Days_change_rate.objects.all():
            for country in Country.objects.all():
                confirmed = 0
                deaths = 0
                recovered = 0
                active = 0
                infos = Covid_info.objects.filter(date=day, country=country)
                for item in infos:
                    confirmed += item.confirmed
                    deaths += item.deaths
                    recovered += item.recovered
                    active += item.active
                    item.delete()
                Covid_info(country=country, date=day, confirmed=confirmed, deaths=deaths, recovered=recovered, active=active).save()



def params_generate():
    return {
        'from': '2020-01-01T00:00:00Z',
        'to': '2020-12-31T00:00:00Z'
    }


def send_request():
    try:
        api = requests.get(url='https://api.covid19api.com/countries')
    except:
        return None
    response = api.json()
    for country in response:
        k = 0
        while True:
            try:
                api_covid_info = requests.get(url=f'https://api.covid19api.com/country/{country["Slug"]}',
                                              params=params_generate())
                break
            except:
                k += 1
                if k > 10:
                    break
                pass
        covid_info_response = api_covid_info.json()
        country_obj = Country(country=country["Slug"])
        country_obj.save()
        for info in covid_info_response:
            try:
                covid_info_obj = Covid_info(country=country_obj,
                                            date=Days_change_rate.objects.get(date=info['Date'][:10]),
                                            confirmed=info['Confirmed'],
                                            deaths=info['Deaths'],
                                            recovered=info['Recovered'],
                                            active=info['Active'], )
                covid_info_obj.save()
            except TypeError:
                continue
