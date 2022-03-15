from .middleware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests



# Create your views here.


@api_view(['GET'])
def get_weather(request):

    # fetching user's ip adress
    ip = get_client_ip(request)
    g = GeoIP2(path='/home/mustafa/MyProjects/nexdegree/GeoLite2-City.mmdb')

    # getting user's location
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    API_key = '8f2a4f38fd48a66d4768530a95e0bb5b'

    #fetching the weather of the user's location
    weather_api = f'api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    curr_weather = requests.get(weather_api)


    return Response({'IP Address ':ip, 'City ': city, 'Current Weather ': curr_weather})