from trubrics.integrations.streamlit import FeedbackCollector
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
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# Configure user feedback

#collector = FeedbackCollector()


#feedback.dict() if feedback else None

def get_input():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_input()

# Response output #
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    response = agent(prompt)
    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.user_input.append(user_input)
        st.session_state.bot_response.append(response)
#        feedback = collector.st_feedback(
#            feedback_type = 'thumbs',
#            path = 'feedback.json'
#        )

    if st.session_state['bot_response']:
        for i in range(len(st.session_state['bot_response'])):
            message(st.session_state['user_input'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['bot_response'][i], key=str(i))
