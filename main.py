import os
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from tools.linkedin_url import linkedin_url
from tools.webscrap import webscrap

load_dotenv()

def generate_profile_summary_and_facts_single_step(name):
    # Create LLM object
    llm = ChatGroq(model = "llama-3.2-11b-text-preview")
    
    # Create Tool
    tools = [linkedin_url, webscrap]
    
    # React prompt
    react_prompt = hub.pull("hwchase17/react")
    
    # React agent
    agent = create_react_agent(
        tools = tools,
        llm = llm,
        prompt = react_prompt,
    )
    
    # Execute agent
    agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    prompt = f"""
    You are an intelligent assistant. Given a Person's {name} Your task is to generate:
    - A brief LinkedIn summary highlighting key aspects of the profile.
    - Two interesting facts about the person derived from the profile.
    - Linked in Profile PIC URL

    Please provide the final output as a JSON object with keys 'summary' and 'interesting_facts'.
    """
    
    result = agent_executer.invoke(input = {"input":prompt})
    
    return result

if __name__ == "__main__":
    name = input("Enter the full name: ")
    result = generate_profile_summary_and_facts_single_step(name)
    print("Generated Output:\n", result)