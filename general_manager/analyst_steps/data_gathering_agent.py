# general_manager/analyst_steps/data_gathering_agent.py
# Step 1 of the analysis workflow: Fetches the NFL schedule.

from google.adk.agents import LlmAgent
from tools import schedule_api_tool

# Define the agent directly as a static instance
data_gathering_agent = LlmAgent(
    name="data_gathering_agent",
    model="gemini-2.5-pro",
    description="A specialist agent for fetching the official NFL schedule from an API.",
    instruction="""
    You are a data retrieval specialist. Your only job is to use the `fetch_schedule_from_api`
    tool to get the official NFL schedule for the season and week you are given.
    
    Return only the direct, unmodified JSON output from the tool.
    """,
    tools=[schedule_api_tool.fetch_schedule_from_api],
    output_key="nfl_schedule" # The output will be passed to the next agent in the sequence.
)
