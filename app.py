from pathlib import Path
import requests
import pytz
from datetime import datetime

import re
import os
import streamlit as st
import matplotlib.pyplot as plt
import openai

from backend.brian import fetch_brian
from backend.weather import get_better_weather_data
from backend.geoloc import geocode, get_timezone, parse_location
from backend.dalle import generate_illustration
from backend.plotting import plot_weather_time_series, interactive_plot
from backend.gpt import generate_answer

APP_NAME = "MelXior"


# set app name
st.set_page_config(page_title=APP_NAME, page_icon=":sunny:")

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    # Exception handling if OPENAI_API_KEY is not set
    st.error(
        "You need to set your OpenAI API key in the environment variable OPENAI_API_KEY." \
        " For example, you can run `export OPENAI_API_KEY=sk-...` in your terminal."
    )
    st.stop()


######## Part 1: real-time audio (question) to text.

st.title(f"Ask {APP_NAME} a weather question!")
original_question = st.text_input("Enter text", "I wanted to go to Bryce Canyon tomorrow morning. Will it rain?")


######## Part 2: text to text (identify location).

context = original_question
prompt = f"{original_question} Ignore the previous question. \
    What city does the above refer to? What state does the above refer to? What country does it refer to? \
    Respond with city, state, country:"


loc = generate_answer(prompt, temperature=0)

# setting default location, when it is not specific
if ('non-specific' in loc) or ('city is Tomorrow' in loc)\
    or ('question is too vague' in loc) or ('city is unknown' in loc)\
    or ('city is Tomorrow' in loc):
    prompt = f"{original_question} Ignore the previous question. \
    I set my default location to San Francisco, CA, United States. What state does the above refer to? What country does it refer to? \
    Respond with city, state, country:"

    loc = generate_answer(prompt, temperature=0)[2:]

city, state, country_code = parse_location(loc)

data = geocode(city=city, state=state, country_code=country_code)
lat, lon = data['lat'], data['lon']

# Extract time
timezone = get_timezone(lat, lon)
cur = datetime.now(pytz.timezone(timezone))
current_date = cur.strftime("%Y-%m-%d")
current_time = cur.strftime("%I:%M %p")

context = original_question
prompt = f"""It is {current_time}. 
    {original_question} How many hours from now does my question refer to?"""

hours = generate_answer(prompt, temperature=0.6)

try:
    hours = int(re.findall(r'\d+', hours)[0])
except:
    hours = 0

st.write(f"Location: {loc},   Time: {hours} hours in the future")
# st.write(f"Current datetime: {current_time, current_date}")

data = geocode(city=city, state=state, country_code=country_code)
lat, lon = data['lat'], data['lon']


########  Part 3: get the weather forecast

data_dir = Path('./data/era5/')
raw_variables, time_series = get_better_weather_data(data_dir, lat, lon)

final_prompt = raw_variables + f"\n Given the above information, {original_question}. Elaborate on the answer."
response = generate_answer(final_prompt, temperature=0.8)

weather_explainer = f"{raw_variables}. Summarize the weather. What should you wear? How should you prepare? Based on the weather, is it better to walk, bike, drive or take public transportation?"
weather_explainer = generate_answer(weather_explainer, temperature=0.8)


########  Part 4: return audio and weather information

session = requests.Session()

funny_mode = "funny meme" in original_question.lower()

st.subheader(f"{APP_NAME}'s summary:")
st.write(f"{weather_explainer}")
audio = fetch_brian(session, weather_explainer, funny_mode=funny_mode)
st.audio(audio, format="audio/wav")

st.subheader(f"{APP_NAME}'s response:")
st.write(f"{response}")
audio = fetch_brian(session, response, funny_mode=funny_mode)
st.audio(audio, format="audio/wav")

st.subheader("Weather predictions")
image = plt.imread("./assets/earth.png")
fig = plot_weather_time_series(time_series)

st.pyplot(fig=fig, clear_figure=True)

st.subheader("Precipitation forecast")
st.pydeck_chart(interactive_plot(lat, lon))

st.text(f"Weather data found: {raw_variables}\nCoordinates: {lat}, {lon}")
        #st.image(image, caption="MelXior", width=400) As we are using Part 5, we dont need this image

## Part 5 Generate the weather summary again (add city to the prompt) using GPT3 and return an image from Dalle
prompt = f"{weather_explainer} in the city of {city}. Summarize this."
call_dalle_prompt = generate_answer(prompt, temperature=0.8)
url = generate_illustration(call_dalle_prompt)

# center the image
st.image(url, caption=f"An artistic representation of {loc} by OpenAI's Dall-E")