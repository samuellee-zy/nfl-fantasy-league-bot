# general_manager/analyst_steps/player_research_agent.py
# Step 2 of the analysis workflow: Researches each player against the schedule.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from ...tools import scout_agent
from ..scouting_assistant_agent import scouting_assistant_agent
import datetime

# Create a tool from the scouting_assistant_agent
scout_tool = AgentTool(agent=scouting_assistant_agent)

# Define the agent directly as a static instance
player_research_agent = LlmAgent(
    name="player_research_agent",
    model="gemini-2.5-pro",
    description="Researches each player on a roster using the provided NFL schedule.",
    instruction=f"""
    You are a fantasy football analyst. Your input will be a JSON string of the official NFL schedule.
    Your task is to perform detailed research on each key player on a user's roster.
    The current year is {datetime.date.today().year}.

    **Process:**
    1.  Your input is the NFL schedule. You MUST PRESERVE this information for the next step.
    2.  First, get the user's roster using the `get_roster` tool.
    3.  For each key player on that roster, you MUST perform the following research:
        a. The latest news and injury updates (via the `scouting_assistant` tool).
        b. **CRITICAL:** Historical stats for the current season and the two previous seasons. You MUST call the `get_player_historical_stats` tool separately for each of the three years.
    4.  **CRITICAL OUTPUT FORMAT:** You MUST format your final output as a single block of text containing three distinct sections, clearly separated by markdown headers:
    
        ### NFL Schedule
        [Paste the original, unmodified NFL schedule JSON string from your input here]
        
        ### User Roster
        [Paste the user roster data you fetched here]
        
        ### Player Research Summary
        [Compile all of your research into a comprehensive summary here]
    """,
    tools=[
        scout_tool,
        scout_agent.get_roster,
        scout_agent.get_player_historical_stats
    ]
)

