from django.db import models


class Days_change_rate(models.Model):
    date = models.DateField()
    rate = models.CharField(max_length=5)

    def __str__(self):
        return str(self.date)


class Change_rate(models.Model):
    rate = models.CharField(max_length=3)
    rate_value = models.FloatField()
    date = models.ForeignKey(Days_change_rate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}<->{self.rate}<->{self.rate_value}"


class Country(models.Model):
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.country


class Covid_info(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.ForeignKey(Days_change_rate, on_delete=models.CASCADE)
    confirmed = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    active = models.IntegerField()

    def __str__(self):
        return f"{self.country}<->{self.date}"
