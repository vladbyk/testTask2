from datetime import timedelta, date

from django.core.management import BaseCommand
import requests
from parser.models import Days_change_rate, Change_rate


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_request()


def params_generate():
    return {
        'app_id': '2c821c2f76eb4c0db94307f6829cccc1',
        'prettyprint': 1,
    }


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def send_request():
    start_date = date(2020, 1, 1)
    end_date = date(2020, 12, 31)
    for single_date in daterange(start_date, end_date):
        k = 0
        while True:
            try:
                api = requests.get(
                    url=f'https://openexchangerates.org/api/historical/2020-{single_date.strftime("%m-%d")}.json',
                    params=params_generate())
                break
            except:
                k += 1
                if k > 10:
                    break
                pass
        response = api.json()
        object_date = Days_change_rate(date=single_date.strftime("%Y-%m-%d"), rate=response['base'])
        object_date.save()
        for rate, rate_value in response['rates'].items():
            Change_rate(rate=rate, rate_value=rate_value, date=object_date).save()
