import requests
import numpy as np
import pytz
import streamlit as st
import os

from datetime import datetime
from timezonefinder import TimezoneFinder

# Openweatherdata personal key, use it at will it's free
try:
    API_KEY = os.environ["OPENWEATHERMAP_API_KEY"]
except:
    API_KEY = None


def geocode(city=None, state=None, country_code=None, limit=5, api_key=API_KEY):
    """
    Given a city, state, and country, return the latitude and longitude and other data
    """
    if city and state and country_code:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country_code}&limit={limit}&appid={api_key}"
    elif city and country_code:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit={limit}&appid={api_key}"
    else:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"

    # get the response
    response = requests.get(url)
    data = eval(response.text)[0]
    return data


def reverse_geocode(  lat=0,
                      lon=0,
                      return_full_response=False,
                      api_key=API_KEY):
    """
    Given a latitude and longitude, return the city, state, and country code
    """
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
    response = requests.get(url)
    if return_full_response:
        return response
    data = eval(response.text)[0]
    return data


def parse_location(loc):
    city, state, country_code = None, None, None
    if " is " in loc:
        try:
            _, loc = loc.split("The city is")
            city, loc = loc.split(", the state is")
            state, country_code = loc.split(", and the country is the")
        except: pass
    else:
        location = loc.split(",")
        if len(location) == 1:
            city = location[0]
        elif len(location) == 2:
            city, country_code = location[0], location[1]
        elif len(location) == 3:
            city, state, country_code = location[0], location[1], location[2]
    return city, state, country_code


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


def get_currenttime(lat, lon):
    timezone = get_timezone(lat, lon)

    current_time = datetime.now(pytz.timezone(timezone))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def parse_location(loc):
    city, state, country_code = None, None, None
    st.write(loc)
    if " is " in loc:
        try:
            _, loc = loc.split("The city is")
            city, loc = loc.split(", the state is")
            state, country_code = loc.split(", and the country is the")
        except: pass
    else:
        location = loc.split(",")
        if len(location) == 1:
            city = location[0]
            st.write(f"I think you are asking about: {city}")
        elif len(location) == 2:
            city, country_code = location[0], location[1]
            st.write(f"I think you are asking about: {city}, {country_code}")
        elif len(location) == 3:
            city, state, country_code = location[0], location[1], location[2]
            st.write(f"I think you are asking about: {city}, {state}, {country_code}")
    return city, state, country_code


def get_closest_idxs(lat_idx, lon_idx, num_pixels=100, max_lon_idx=1440, max_lat_idx=721):
    """
    Given a 2D array, get the data indexes around a given location with a given number of pixels.
    """
    lat_min = lat_idx - int(num_pixels / 2)
    lat_max = lat_idx + int(num_pixels / 2)
    lon_min = lon_idx - num_pixels
    lon_max = lon_idx + num_pixels

    if lat_min < 0:
        lat_min = 0
    if lat_max > max_lat_idx:
        lat_max = max_lat_idx
    if lon_min < 0:
        lon_min += max_lon_idx
    if lon_max > max_lon_idx:
        lon_max -= max_lon_idx

    # Get indexes of the data
    if lat_min < lat_max:
        lat_idxs = np.arange(lat_min, lat_max)
    else:
        lat_idxs = np.concatenate((np.arange(lat_min, max_lat_idx), np.arange(0, lat_max)))

    if lon_min < lon_max:
        lon_idxs = np.arange(lon_min, lon_max)
    else:
        lon_idxs = np.concatenate((np.arange(lon_min, max_lon_idx), np.arange(0, lon_max)))
    return lat_idxs, lon_idxs


def get_closest_data_from_location(lat, lon, data, num_pixels=100, **kwargs):
    """
    Given a 2D array, get the data around a given location with a given number of pixels.
    """
    lat_idx, lon_idx = get_closest_pixel(lat, lon)
    lat_idxs, lon_idxs = get_closest_idxs(lat_idx, lon_idx, num_pixels, **kwargs)
    return data[lat_idxs, :][:, lon_idxs]


if __name__ == "__main__":
    print(get_timezone(40.7128, -74.0060))