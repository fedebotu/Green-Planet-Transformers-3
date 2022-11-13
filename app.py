import streamlit as st

# A simple Streamlit app that showcases the functionality of the FAQ generator

st.title("Green Planet Transformer 3 - TODO final app with calls 🚀")

st.write(
    "Use this tool to generate FAQs for your Climate Change education materials. "
    "Inspired by [Project Regeneration Nexus](https://regeneration.org/nexus), "
    "it uses OpenAI's APIs to generate questions and answers."
)
st.write(
    "The app is currently a POC. It extracts text from the selected nexus solution, "
    "chunks the text, embeds those chunks, and uses prompt-chaining to generate "
    "questions and answers pertaining to the text."
)

#  Extracted using GPT by pasting the HTML blob into playground and prompting with
#  "Extract all hrefs from above into a python list" :)
hrefs = [
    "/nexus/afforestation",
    "/nexus/agroecology",
    "/nexus/agroforestry",
    "/nexus/asparagopsis",
    "/nexus/azolla-fern",
    "/nexus/bamboo",
    "/nexus/beavers",
    "/nexus/biochar",
    "/nexus/buildings",
    "/nexus/clean-cookstoves",
    "/nexus/compost",
    "/nexus/degraded-land-restoration",
    "/nexus/eating-plants",
    "/nexus/education-girls",
    "/nexus/electric-vehicles",
    "/nexus/electrify-everything",
    "/nexus/energy-storage",
    "/nexus/fifteen-minute-city",
    "/nexus/fire-ecology",
    "/nexus/grasslands",
    "/nexus/heat-pumps",
    "/nexus/mangroves",
    "/nexus/marine-protected-areas",
    "/nexus/micromobility",
    "/nexus/nature-of-cities",
    "/nexus/net-zero-cities",
    "/nexus/offsets",
    "/nexus/ocean-farming",
    "/nexus/regenerative-agriculture",
    "/nexus/seaforestation",
    "/nexus/seagrasses",
    "/nexus/silvopasture",
    "/nexus/smart-microgrids",
    "/nexus/solar",
    "/nexus/tidal-salt-marshes",
    "/nexus/tropical-forests",
    "/nexus/urban-farming",
    "/nexus/urban-mobility",
    "/nexus/wetlands",
    "/nexus/wind",
]

top_similar = 4
left, right = st.columns(2)
form = left.form("template_form")
# url_input = form.text_input("Project Regeneration Nexus solutions on", value="regeneration.org/nexus/agroecology")
url_input = form.selectbox(
    "Project Regeneration Nexus Solutions on",
    list(map(lambda href: href.split("/")[-1], hrefs)),
)
topic_input = form.text_input(
    "Relevant Topic (optional)",
    placeholder="food diversity",
    value="action items",
)
audience_input = form.text_input(
    "Audience (optional)", placeholder="students", value="students"
)
num_questions_input = form.number_input(
    "Number of Questions", min_value=2, max_value=5, value=3
)
submit = form.form_submit_button("Generate FAQs")
