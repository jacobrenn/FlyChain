from langchain.agents import initialize_agent, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, LLMChain
from .utils import get_openai_api_key
from .tools import my_tools

def create_agent(
        model = 'text-davinci-003',
        tools = my_tools,
        temperature = 0,
        chat_history = False
):
    
    # Initiate regular model if not davinci
    if model in ['text-davinci-003']:
        llm = OpenAI(model_name = model, openai_api_key = get_openai_api_key(), temperature = temperature)

    # Initiate chat model if not davinci
    elif model in ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4']:
        llm = ChatOpenAI(model_name = model, openai_api_key = get_openai_api_key(), temperature = temperature)

    if chat_history:
        prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
        suffix = """Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )
        memory = ConversationBufferMemory(memory_key="chat_history")
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        return AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=memory
        )
    else:
        return initialize_agent(
            tools = tools,
            llm = llm,
            verbose = True
        )

