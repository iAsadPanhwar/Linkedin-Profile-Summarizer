import os
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from tools.linkedin_url import linkedin_url
from tools.webscrap import webscrap

load_dotenv()

