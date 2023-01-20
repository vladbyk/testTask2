from rest_framework import serializers
from .models import Days_change_rate, Change_rate, Country, Covid_info


class Days_change_rateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days_change_rate
        fields = '__all__'


class Change_rateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change_rate
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class Covid_infoSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    date = Days_change_rateSerializer()

    class Meta:
        model = Covid_info
        fields = '__all__'
