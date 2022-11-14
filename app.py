from pathlib import Path
import requests
import pytz
from datetime import datetime

import os
import re
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import h5py
import openai

from backend.brian import fetch_brian
from backend.geoloc import geocode, reverse_geocode, get_currenttime, parse_location
from backend.prompting import default_prompt, prompt_location_from_user_input
from backend.weather import get_closest_pixel, get_weather_data, plot_weather_time_series


# [MP] this should probably be a script argument
openai.api_key = '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'


######## Part 1: real-time audio (question) to text.
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "streamlit_audio_recorder/st_audiorec/frontend/build")

# [MP] Placeholder
st.title("Ask MelXior a weather question!")
original_question = st.text_input("Enter text", "I wanted to go to Bryce Canyon tomorrow. Will it rain there?")


######## Part 2: text to text (identify location).
loc = prompt_location_from_user_input(original_question)
city, state, country_code = parse_location(loc)
data = geocode(city=city, state=state, country_code=country_code)
lat, lon = data['lat'], data['lon']

# Get the coordinates
current_time = get_currenttime(lat, lon)
context = original_question
prompt = f"{original_question} Ignore the previous question. \
    Given that it is now {current_time}, How many hours in the future does the above refer to? \
    Respond with number of hours"
response = default_prompt(prompt)

hours = response['choices'][0]['text'][2:]
try:
    hours = int(re.findall(r'\d+', hours)[0])
except:
    hours = 0

st.write(f'{current_time}')
st.write(f"Location: {loc},   Time: {hours} hours in the future")
data = geocode(city=city, state=state, country_code=country_code)
lat, lon = data['lat'], data['lon']

########  Part 3: get the weather forecast
data_dir = Path('./data/era5/')
raw_variables, time_series, time_series_str = get_weather_data(data_dir, lat, lon)

final_prompt = raw_variables + f"\n Given the above information, {original_question}"
response = default_prompt(final_prompt)
response = response['choices'][0]['text']

prompt_explainer = f"{raw_variables} {response} Why is this true?"
response_explainer = default_prompt(prompt_explainer)
response_explainer = response_explainer['choices'][0]['text']

weather_explainer = f"{time_series_str}. What can we say about the weather given the above information? What should you wear? How should you prepare? Based on the weather, should you walk, bike, drive or take public transportation?"
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

funny_mode = "funny meme" in original_question.lower()

audio = fetch_brian(session, weather_explainer + response, funny_mode=funny_mode)
st.audio(audio, format="audio/wav")

image = plt.imread("./assets/earth.png")
fig = plot_weather_time_series(time_series)

# st.pyplot(fig=fig, caption="measurements for next week", clear_figure=True)
st.text(f"Weather data found: {raw_variables}\nCoordinates: {lat}, {lon}")
st.image(image, caption="MelXior")