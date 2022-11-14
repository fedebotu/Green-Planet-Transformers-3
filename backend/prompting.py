import openai
import streamlit as st

def default_prompt(prompt):
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
    return response

def prompt_location_from_user_input(original_question):
    # [MP] We need a robust way to filter the question and extract the location.
    # For now, we'll assume the query is about a location in the US.
    context = original_question
    prompt = f"{original_question} Ignore the previous question. \
        What city does the above refer to? What state does the above refer to? What country does it refer to? \
        Respond with city, state, country:"

    response = default_prompt(prompt)

    # [MP] ignore newlines at the start
    loc = response['choices'][0]['text'][2:]

    ## setting default location, when it is not specific
    if ('non-specific' in loc) or ('city is Tomorrow' in loc)\
        or ('question is too vague' in loc) or ('city is unknown' in loc)\
        or ('city is Tomorrow' in loc):
        prompt = f"{original_question} Ignore the previous question. \
        I set my default location to San Francisco, CA, United States. What state does the above refer to? What country does it refer to? \
        Respond with city, state, country:"

        response = default_prompt(prompt)
        loc = response['choices'][0]['text'][2:]
    return loc

