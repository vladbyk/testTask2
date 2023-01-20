import json

import matplotlib
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from .models import Country, Days_change_rate, Change_rate, Covid_info
from .serializers import CountrySerializer, Days_change_rateSerializer, Change_rateSerializer, Covid_infoSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def country_view(request, pk):
    if request.method == 'POST':
        serializer_country = CountrySerializer(data=request.data)
        if serializer_country.is_valid():
            serializer_country.save()
            return Response(serializer_country.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_country.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        country = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_country = CountrySerializer(country)
        return Response(serializer_country.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer_country = CountrySerializer(country, data=request.data)
        if serializer_country.is_valid():
            serializer_country.save()
            return Response(serializer_country.data)
        return Response(serializer_country.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def days_change_rate_view(request, pk):
    if request.method == 'POST':
        serializer_days_change_rate = Days_change_rateSerializer(data=request.data)
        if serializer_days_change_rate.is_valid():
            serializer_days_change_rate.save()
            return Response(serializer_days_change_rate.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_days_change_rate.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        days_change_rate = Days_change_rate.objects.get(pk=pk)
    except Days_change_rate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_days_change_rate = Days_change_rateSerializer(days_change_rate)
        return Response(serializer_days_change_rate.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer_days_change_rate = Days_change_rateSerializer(days_change_rate, data=request.data)
        if serializer_days_change_rate.is_valid():
            serializer_days_change_rate.save()
            return Response(serializer_days_change_rate.data)
        return Response(serializer_days_change_rate.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        days_change_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def change_rate_view(request, pk):
    if request.method == 'POST':
        serializer_change_rate = Change_rateSerializer(data=request.data)
        if serializer_change_rate.is_valid():
            serializer_change_rate.save()
            return Response(serializer_change_rate.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_change_rate.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        change_rate = Change_rate.objects.get(pk=pk)
    except Change_rate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_change_rate = Change_rateSerializer(change_rate)
        return Response(serializer_change_rate.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer_change_rate = Change_rateSerializer(change_rate, data=request.data)
        if serializer_change_rate.is_valid():
            serializer_change_rate.save()
            return Response(serializer_change_rate.data)
        return Response(serializer_change_rate.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        change_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def covid_info_view(request, pk):
    if request.method == 'POST':
        serializer_covid_info = Covid_infoSerializer(data=request.data)
        if serializer_covid_info.is_valid():
            serializer_covid_info.save()
            return Response(serializer_covid_info.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_covid_info.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        covid_info = Covid_info.objects.get(pk=pk)
    except Covid_info.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_covid_info = Covid_infoSerializer(covid_info)
        return Response(serializer_covid_info.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer_covid_info = Covid_infoSerializer(covid_info, data=request.data)
        if serializer_covid_info.is_valid():
            serializer_covid_info.save()
            return Response(serializer_covid_info.data)
        return Response(serializer_covid_info.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        covid_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plot_view(request):
    if request.method == 'GET':
        params = request.query_params
        matplotlib.use('agg')
        plt.style.use(['ggplot'])
        country = Country.objects.get(country=params['country'])
        covid_info = Covid_info.objects.filter(country__pk=country.pk, date__date__gte=params['start'],
                                               date__date__lte=params['end']).order_by('date__date')
        x = np.array(covid_info.values_list('date__date', flat=True))
        y = np.array(covid_info.values_list('confirmed', flat=True))
        y1 = np.array(covid_info.values_list('deaths', flat=True))
        y2 = np.array(covid_info.values_list('recovered', flat=True))
        y3 = np.array(covid_info.values_list('active', flat=True))
        plt.figure(figsize=(14, 8), dpi=120)
        plt.xlabel('Дата', fontsize=20, color='grey')
        plt.ylabel('Кол-во человек', fontsize=20, color='grey')
        plt.title(country.country.capitalize(), fontsize=30)
        plt.plot(x, y, '-g', label='Кол-во подтверждённых случаев', linewidth=3)
        plt.plot(x, y1, '-k', label='Кол-во погибших', linewidth=3)
        plt.plot(x, y2, '-r', label='Кол-во вылеченных', linewidth=3)
        plt.plot(x, y3, '-b', label='Кол-во больных в этот день', linewidth=3)
        plt.legend()
        plt.xticks([x[i] for i in range(0, len(x), 1 if len(x) < 10 else int(len(x) / 10))])
        plt.locator_params(axis='y', nbins=10)
        image_io = io.BytesIO()
        plt.savefig(image_io, transparent=True)
        image_io.seek(0)
        base64_img_data = base64.b64encode(image_io.read())
        return Response({'bytes': base64_img_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plot_rates_view(request, rate):
    if request.method == 'GET':
        file = open('parser/utils/currency_info/currency.json', encoding='utf8')
        currency = json.load(file)
        file.close()
        rates = Change_rate.objects.filter(rate=rate)
        matplotlib.use('agg')
        plt.style.use(['ggplot'])
        x = np.array(rates.values_list('date__date', flat=True))
        y = np.array(rates.values_list('rate_value', flat=True), dtype="float")
        plt.figure(figsize=(14, 8), dpi=120)
        plt.xlabel('Дата', fontsize=20, color='grey')
        plt.ylabel('Курс валюты к 1 доллару', fontsize=20, color='grey')
        plt.title(currency[rate][1].capitalize(), fontsize=30)
        plt.plot(x, y, '-r', label=currency[rate][0], linewidth=3)
        plt.legend()
        plt.xticks([x[i] for i in range(0, len(x), 1 if len(x) < 10 else int(len(x) / 10))])
        plt.locator_params(axis='y', nbins=10)
        image_io = io.BytesIO()
        plt.savefig(image_io, transparent=True)
        image_io.seek(0)
        base64_img_data = base64.b64encode(image_io.read())
        return Response({'bytes': base64_img_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rates_view(request):
    if request.method == 'GET':
        file = open('parser/utils/currency_info/currency.json', encoding='utf8')
        currency = json.load(file)
        file.close()
        rates = currency.keys()
        return Response({'rates': rates}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def countries_view(request):
    if request.method == 'GET':
        countres = Country.objects.all()
        serializer = CountrySerializer(countres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
