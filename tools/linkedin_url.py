import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
# Load environment variables
load_dotenv()

# Create a function to get LinkedIn URL from a given name
def get_linkedin_url(name):
    """
    This function searches for a Linkedin url
    """
    
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res
    
# Convert function to a tool
linkedin_url = Tool(
    name = "Search Google for LinkedIn URL",
    func = get_linkedin_url,
    description = "This tool is useful when you need to search profile url for a user."
)