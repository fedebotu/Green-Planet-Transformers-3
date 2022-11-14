from pathlib import Path
import requests

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import h5py
import openai

from backend.brian import fetch_brian
from backend.weather import get_closest_pixel, get_weather_data, plot_weather_time_series
from backend.dalle import generate_illustration

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

data_dir = Path('./data/era5/')
raw_variables, time_series, time_series_str = get_weather_data(data_dir, lat, lon)


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


audio = fetch_brian(session, weather_explainer + response, funny_mode=True)
st.audio(audio, format="audio/wav")


image = plt.imread("./assets/earth.png")
# fig = plot_weather_time_series(time_series)


st.pyplot(fig=fig, caption="measurements for next week", clear_figure=True)
st.text(f"Weather data found: {raw_variables}\nCoordinates: {lat}, {lon}")
#st.image(image, caption="MelXior")

## Part 5 Generate the weather summary again (add city to the prompt) using GPT3 and return an image from Dalle
prompt = f"{weather_explainer} in the city of {city}. Summarize this."
call_dalle_prompt = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.8,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"] #\n
)
url = generate_illustration(call_dalle_prompt['choices'][0]['text'].strip())
st.image(url,width=400)