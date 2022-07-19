import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&APPID=53cc655a14666b4965050fe2d13ccc9d'
    error = ""
    message = ""
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            count = City.objects.filter(name=new_city).count()
            if count:
                error = 'Этот город найден. Введите другой город'
            else:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    error = 'Введите другой город. Такого города нет'
        if error:
            message = error
    form = CityForm()
    cities = City.objects.all()
    data = []
    for city in cities:
        response = requests.get(url.format(city)).json()
        city = {
            'pk': city.pk,
            'icon': response['weather'][0]['icon'],
            'city': city.name,
            'country_code': response['sys']['country'],
            'temperature': response['main']['temp'],
            'feels_like': response['main']['feels_like'],
            'description': response['weather'][0]['description'],
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure'],
        }
        data.append(city)

    return render(request, 'city/weather.html', {'data': data,
                                                 'form': form,
                                                 'message': message,
                                                 }
                  )


def delete_city(request, pk):
    City.objects.get(pk=pk).delete()
    return redirect('home')