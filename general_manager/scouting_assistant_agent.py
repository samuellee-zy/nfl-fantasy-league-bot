# agents/scouting_assistant_agent.py
# This new agent is a specialist whose only job is to use the google_search tool.
# This respects the ADK limitation of not mixing built-in and custom tools.

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

def create_agent():
    """Factory function to create the Scouting Assistant agent."""
    return LlmAgent(
        # **CHANGE**: Standardize name to snake_case.
        name="scouting_assistant",
        model="gemini-2.5-flash",
        description="A specialist assistant that performs Google Searches to find the latest news, articles, and injury updates about NFL players.",
        instruction="""
        You are a scouting assistant. Your only function is to take a query from another agent
        and use the google_search tool to find relevant, up-to-date information.
        Return the search results clearly and concisely.
        """,
        tools=[google_search],
    )

