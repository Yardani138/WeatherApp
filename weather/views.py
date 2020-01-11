import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    appid = 'YOUR API KEY'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if(res["cod"] == 200):
            city_info = {
                'city': res["name"],
                'temp': int(res["main"]["temp"]),
                'feels': int(res["main"]["feels_like"]),
                'icon': res["weather"][0]["icon"],
                'visibility': res["visibility"],
                'country': res["sys"]["country"]
            }

            all_cities.append(city_info)
        else:
            print("City with that name doesn't exist")

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)

def info(request):
    return render(request, 'weather/info.html')

def donate(request):
    return render(request, 'weather/donate.html')
