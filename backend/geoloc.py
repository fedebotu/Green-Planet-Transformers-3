import requests
import numpy as np
from timezonefinder import TimezoneFinder


# Openweatherdata personal key, use it at will it's free
API_KEY = "e83b3c4c08285bf87b99f9bbc0abe3f0" # need to wait for activation


def geocode(    city=None, 
                state=None, 
                country_code=None, 
                limit=5, 
                api_key=API_KEY):
    """
    Given a city, state, and country, return the latitude and longitude and other data
    """

    if city and state and country_code:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country_code}&limit={limit}&appid={api_key}"
    elif city and country_code: 
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit={limit}&appid={api_key}"
    elif city: 
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"
    
    # get the response
    response = requests.get(url)
    data = eval(response.text)[0]
    return data


def reverse_geocode(  lat=0,
                      lon=0, 
                      return_full_response=False,
                      api_key=None):
    """
    Given a latitude and longitude, return the city, state, and country code
    """
    api_key = API_KEY if api_key is None else api_key
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if return_full_response:
        return response
    data = eval(response.text)[0]
    return data


# Get latitudes and longitudes with the same shape as the data
lats = np.linspace(90, -90, 721)
longs = np.linspace(-180, 180, 1440)

def get_closest_pixel(lat, lon, lats=lats, longs=longs):
    """
    Given a latitude and longitude, return the closest pixel
    Get the closest pixel (best way would be to interpolate - TODO)
    """
    lat_idx = np.argmin(np.abs(lats - lat))
    long_idx = np.argmin(np.abs(longs - (lon + 180)))
    return lat_idx, long_idx


def get_timezone(lat, lon):
    """
    Given a latitude and longitude, return the timezone
    """
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)


if __name__ == "__main__":
    print(get_timezone(40.7128, -74.0060))