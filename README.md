# Green Planet Transformers 3

[![build](https://github.com/fedebotu/Green-Planet-Transformers-3/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/fedebotu/Green-Planet-Transformers-3/actions/workflows/main.yml)

Repository for OpenAI's Climate Hackathon :>>>>>**TODO**<<<<<<: description


## How does it work?

:>>>>>**TODO**<<<<<<:

## Usage

<div class="tenor-gif-embed" data-postid="20733328" data-share-method="host" data-aspect-ratio="1.11111" data-width="100%"><a href="https://tenor.com/view/placeholder-text-animated-word-gif-20733328">Placeholder Text GIF</a>from <a href="https://tenor.com/search/placeholder-gifs">Placeholder GIFs</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>

### Getting started 

To run this app locally, follow the steps:

1. Clone the repository (`git clone git@github.com:fedebotu/Green-Planet-Transformers-3.git`)
2. Create a virtual environment (`python3 -m venv venv && source venv/bin/activate`)
2. Install the requirements by running `make install`
3. Ensure your OpenAI API key is set as an environment variable `OPENAI_API_KEY` 
(see best practices around API key safety [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety))
4. Run the [streamlit](https://streamlit.io/) app by running `make run`
5. Open the app in your browser at `http://localhost:8501`


### Obtain FourCastNet prediction data

Given that real time data in this format is not easily available and would require access to real-time meteorological data from the globe, we use predictions from historical data located under [`data/era5`](/data/) for ease of use:
- `sample.h5`: ~80 MB, contains all weather variables for the globe in one time slice (provided in Repo)
- `single_week.h5`: ~2.4 GB, contains all weather variables for the globe for one week to [[download here](https://drive.google.com/file/d/1vbR1O3Zf1fWDazs8r5n-Uoa31OLeIKeS/view?usp=sharing)]

> Note that when deployed in real time, the model needs to be run only once every 6 hours. We save inference predictions and then query them in our app, as in the files above to greatly speed up the pipeline!



### Install app requirements.txt

If you encounter issues when installing `pyaudio`, run the following: `sudo apt install portaudio19-dev`.

#### Example Qs to ask MelXior

* I wanted to go to X tomorrow. Will it rain there?
* I wanted to go to X tomorrow. Can I wear a t-shirt?
* I wanted to go to X tomorrow. Can I bike there?

<span class="caption">Example from FourCastNet data</span>
<div align="center">
  <img src="assets/rh.gif" alt="animated"/>
</div>

- - -


<div align="center">
<img src="assets/earth.png" alt="drawing" width="25%"/>
</div>
