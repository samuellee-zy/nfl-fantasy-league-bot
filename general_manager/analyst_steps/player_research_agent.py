# general_manager/analyst_steps/player_research_agent.py
# Step 2 of the analysis workflow: Researches each player against the schedule.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from tools import scout_agent
from ..scouting_assistant_agent import scouting_assistant_agent

# Create a tool from the scouting_assistant_agent
scout_tool = AgentTool(agent=scouting_assistant_agent)

# Define the agent directly as a static instance
player_research_agent = LlmAgent(
    name="player_research_agent",
    model="gemini-2.5-pro",
    description="Researches each player on a roster using the provided NFL schedule.",
    instruction="""
    You are a fantasy football analyst. You will be given a user's roster and the official NFL schedule.
    Your task is to perform detailed research on each key player.

    **Process:**
    1.  First, get the user's roster using the `get_roster` tool.
    2.  For each key player on that roster, use your other tools to find:
        a. The latest news and injury updates (via the `scouting_assistant` tool).
        b. Historical stats for previous seasons (via the `get_player_historical_stats` tool).
    3.  Compile all of this research into a comprehensive text block. This will be passed to the report synthesizer.
    """,
    input_key="nfl_schedule", # Takes the schedule from the previous agent.
    output_key="research_summary", # Passes the output to the next agent.
    tools=[
        scout_tool,
        scout_agent.get_roster,
        scout_agent.get_player_historical_stats
    ]
)