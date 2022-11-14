from pathlib import Path
import requests
import pytz
from datetime import datetime

import re
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import h5py
import openai

from backend.brian import fetch_brian
from backend.weather import get_closest_pixel, get_weather_data, plot_weather_time_series
from backend.geoloc import geocode, reverse_geocode, get_timezone


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

# [MP] ignore newlines at the start
loc = response['choices'][0]['text'][2:]

## setting default location, when it is not specific
if ('non-specific' in loc) or ('city is Tomorrow' in loc)\
    or ('question is too vague' in loc) or ('city is unknown' in loc)\
    or ('city is Tomorrow' in loc):
    prompt = f"{original_question} Ignore the previous question. \
    I set my default location to San Francisco, CA, United States. What state does the above refer to? What country does it refer to? \
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

    loc = response['choices'][0]['text'][2:]


location = loc.split(",")

city, state, country_code = None, None, None
if len(location) == 1:
    city = location[0]
    st.write(f"I think you are asking about: {city}")
elif len(location) == 2:
    city, country_code = location[0], location[1]
    st.write(f"I think you are asking about: {city}, {country_code}")
elif len(location) == 3:
    city, state, country_code = location[0], location[1], location[2]
    st.write(f"I think you are asking about: {city}, {state}, {country_code}")

data = geocode(city=city, state=state, country_code=country_code)
lat, lon = data['lat'], data['lon']


# Extract time
timezone = get_timezone(lat, lon)

current_time = datetime.now(pytz.timezone(timezone))
current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


context = original_question
prompt = f"{original_question} Ignore the previous question. \
    Given that it is now {current_time}, How many hours in the future does the above refer to? \
    Respond with number of hours"

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
raw_variables, time_series = get_weather_data(data_dir, lat, lon)


final_prompt = raw_variables + f"\n Given the above information, {original_question}"

response = openai.Completion.create(
    model="text-davinci-002",
    prompt=final_prompt,
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)

response = response['choices'][0]['text']

prompt_explainer = f"{raw_variables} {response} Why is this true?"

response_explainer = openai.Completion.create(
    model="text-davinci-002",
    prompt=response,
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] 
)

response_explainer = response_explainer['choices'][0]['text']


weather_explainer = f"{raw_variables}. What can we say about the weather given the above information?"

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


st.pyplot(fig=fig, caption="measurements for next week", clear_figure=True)
st.text(f"Weather data found: {raw_variables}\nCoordinates: {lat}, {lon}")
st.image(image, caption="MelXior")