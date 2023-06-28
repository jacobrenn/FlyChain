from langchain.agents import initialize_agent, AgentType
from langchain import OpenAI
from utils import get_openai_api_key
from tools import my_tools

def create_agent(
        model = 'text-davinci-003',
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        tools = my_tools,
        temperature = 0
):
    return initialize_agent(
        tools = tools,
        llm = OpenAI(model_name = model, openai_api_key = get_openai_api_key(), temperature = temperature),
        agent = agent_type,
        verbose = True
    )
