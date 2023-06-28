from langchain.agents import tools, tool

# Create your own tools here
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import ShellTool

@tool
def ddg_search(query):
    """Use this tool to search DuckDuckGo"""

    ddg_search = DuckDuckGoSearchAPIWrapper()
    return ddg_search.run(query)



# Add all of the tools you would like the agent to 
# have access to to this list here
my_tools = [ddg_search, ShellTool()]