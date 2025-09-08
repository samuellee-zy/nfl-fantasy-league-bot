# agents/analyst_steps/player_research_agent.py
# Step 2 of the analysis workflow: Researches each player.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from general_manager import scouting_assistant_agent
from tools import scout_agent

def create_agent():
    """Factory function to create the player research agent."""
    
    scout_tool = AgentTool(agent=scouting_assistant_agent.create_agent())

    return LlmAgent(
        name="player_research_agent",
        model="gemini-2.5-pro", # Uses the powerful model for analysis
        instruction="""
        You are a fantasy football analyst. You will be given a user's roster and the official NFL schedule.
        Your task is to perform detailed research on each player.

        **Process:**
        1.  For each key player on the roster, use your tools to find:
            a. The latest news and injury updates (via the `scouting_assistant` tool).
            b. Historical stats for previous seasons (via the `get_player_historical_stats` tool).
        2.  Compile all of this research into a comprehensive text block.
        """,
        # **FIX**: Removed the invalid 'input_key' argument. The SequentialAgent handles this automatically.
        output_key="research_summary",
        tools=[
            scout_tool,
            scout_agent.get_player_historical_stats
        ]
    )

