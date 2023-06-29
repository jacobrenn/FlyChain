#import trubrics
from trubrics.integrations.streamlit import FeedbackCollector
import json
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from agent import create_agent


agent = create_agent()

st.set_page_config(page_title = 'Flychain')

# Generate empty lists for bot_response and user_input. -> add HTML for interactive feedback
## bot_response stores AI generated responses
if 'bot_response' not in st.session_state:
    st.session_state['bot_response'] = ['How can I help you?']
## user_input stores User's questions
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ['Hi!']

# Layout of input/response containers


response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()

# Configure user feedback
collector = FeedbackCollector(
    component_name = 'default',
    email = None,
    password = None
    )

user_feedback_path = '../user_feedback/feedback.json'

@st.cache_data(allow_output_mutation=True, suppress_st_warning=True)
def get_input():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_input()

# Response output #
## Function for taking user prompt as input followed by producing AI generated responses

@st.cache_data(allow_output_mutation=True, suppress_st_warning=True)
def generate_response(prompt):
    try:
        response = agent.run(input = prompt)
    except:
        response = agent(prompt)
    return response

## Conditional display of AI generated responses as a function of user provided prompts

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.user_input.append(user_input)
        st.session_state.bot_response.append(response)


    if st.session_state['bot_response']:
        for i in range(len(st.session_state['bot_response'])):
            message(st.session_state['user_input'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['bot_response'][i], key=str(i))
            feedback = collector.st_feedback(
                feedback_type = 'thumbs',
                model = 'langchain',
                open_feedback_label="[Optional] Provide additional feedback",
                save_to_trubrics = False
            )

            if feedback:
                # Add 'bot_response' to 'feedback'
                feedback['bot_response'] = st.session_state['bot_response'][i]

                # Load the existing data
                try:
                    with open(user_feedback_path, 'r') as file:
                        data = json.load(file)
                except json.JSONDecodeError:  # if the file is empty, initialize 'data' as an empty list
                    data = []

                # Append the new feedback with the bot's response
                data.append(feedback)

                # Write the new data
                with open(user_feedback_path, 'w') as file:
                    json.dump(data, file, indent=4, default=str)
