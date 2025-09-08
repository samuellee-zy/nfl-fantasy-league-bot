# agents/data_gathering_agent.py
# Defines a specialist agent for fetching external data, like the NFL schedule.

from google.adk.agents import LlmAgent
from tools import schedule_api_tool

def create_agent():
    """Factory function to create the Data Gathering agent."""
    
    return LlmAgent(
        name="data_gathering_agent",
        model="gemini-2.5-pro",
        description="A specialist agent for fetching data. It uses tools to get information like the NFL schedule.",
        instruction="""
        You are a data retrieval specialist. Your only job is to use the tools you have
        to fetch requested information.
        
        When asked for the NFL schedule, you MUST use the `fetch_schedule_from_api` tool.
        Return the direct, unmodified output from the tool.
        """,
        tools=[schedule_api_tool.fetch_schedule_from_api],
    )

