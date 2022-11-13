from pathlib import Path
import requests

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import h5py
import openai

from backend.brian import fetch_brian


# [MP] this should probably be a script argument
openai.api_key = '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' 


######## Part 1: real-time audio (question) to text.

# [MP] Placeholder
st.title("Ask MelXior a weather question!")
original_question = st.text_input("Enter text", "I wanted to go to Bryce Canyon tomorrow. Will it rain there?")


######## Part 2: text to text (identify location).

# [MP] We need a robust way to filter the question and extract the location. 
# For now, we'll assume the query is about a location in the US.
context = original_question
prompt = f"{original_question} Ignore the previous question. \
    What city does the above refer to? What state does the above refer to? What country does it refer to? \
    Respond with city, state, country:"

response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)

loc = response['choices'][0]['text']

st.write(f"I think you are asking about: {loc}")
# [MP] Sometimes GPT responds 
city, state, country = loc.split(",")


# Get the coordinates 
API_KEY = "e83b3c4c08285bf87b99f9bbc0abe3f0" # need to wait for activation

def geocode(    city=None, 
                state=None, 
                country_code=None, 
                limit=5, 
                api_key=API_KEY):
    """
    Given a city, state, and country, return the latitude and longitude and other data
    """

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country_code}&limit={limit}&appid={api_key}"
    
    # get the response
    response = requests.get(url)
    data = eval(response.text)[0]
    return data

data = geocode(city=city, state=state, country_code=country)
lat, lon = data['lat'], data['lon']

########  Part 3: get the weather forecast

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

lat_idx, lon_idx = get_closest_pixel(lat, lon)

data_dir = Path('./data/era5/')

# Open h5py file
f = h5py.File(data_dir / 'sample.h5', 'r')
u = f['u10'][0]
v = f['v10'][0]
temp = f['t2m'][0]

u_sf = u[lat_idx, lon_idx]
v_sf = v[lat_idx, lon_idx]
temp_sf = temp[lat_idx, lon_idx]

prompt = ''

for var in f.keys():
    # add to prompt with value
    if var in ['u10', 'v10', 't2m', 'r850', 'sp', 'mslp', 't850', 'u1000', \
        'v1000', 'z1000', 'u850', 'v850', 'z850', 'u500', 'v500', 'z500', 't500', \
            'z50', 'r500', 'tcwv', 'sst']:
        prompt += f[var].attrs['description'] + " is: {:.2f} \n".format(f[var][0, lat_idx, lon_idx])


final_prompt = prompt + f"\n Given the above information, {original_question}"

response = openai.Completion.create(
    model="text-davinci-002",
    prompt=final_prompt,
    temperature=0.4,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)

response = response['choices'][0]['text']

prompt_explainer = f"{prompt} {response} Why is this true?"

response_explainer = openai.Completion.create(
    model="text-davinci-002",
    prompt=response,
    temperature=0.4,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)

response_explainer = response_explainer['choices'][0]['text']


weather_explainer = f"{prompt}. What can we say about the weather given the above information?"

weather_explainer = openai.Completion.create(
    model="text-davinci-002",
    prompt=weather_explainer,
    temperature=0.4,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)

weather_explainer = weather_explainer['choices'][0]['text']



########  Part 4: return audio and weather information

session = requests.Session()


audio = fetch_brian(session, weather_explainer + response, funny_mode=True)
st.audio(audio, format="audio/wav")

# load and display image
image = plt.imread("./assets/earth.png")

# # display text in text box
# st.title("Text Box")

# st.text(f"{text}")

st.text(f"Weather data found: {prompt}, Coordinates: {lat}, {lon}")