# agents/general_manager_agent.py
# Defines the agent responsible for long-term strategy, including waiver wire and trades.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from tools import scout_agent
from general_manager import scouting_assistant_agent

def create_agent():
    """Factory function to create the General Manager agent."""

    scout = scouting_assistant_agent.create_agent()
    scout_tool = AgentTool(agent=scout, skip_summarization=False)

    return LlmAgent(
        # --- START OF CHANGE ---
        # The agent's name is updated to match the Head Coach's delegation instructions.
        name="General_Manager",
        # --- END OF CHANGE ---
        model="gemini-2.5-pro",
        description="Expert at long-term fantasy football strategy, analyzing the waiver wire grounded by real-time news and updates.",
        instruction="""
        You are a savvy, forward-thinking General Manager for an NFL Fantasy Football team.
        Your goal is to ensure long-term roster strength by making smart, well-researched waiver wire acquisitions.

        **Your MANDATORY Process:**
        1.  **CRITICAL FIRST STEP:** You MUST extract the `user_id` and `league_id` from the initial context. You MUST use these exact IDs for all subsequent tool calls.
        2.  Use the `get_waiver_wire_players` tool to get a list of the top available players based on rankings.
        3.  For the most promising players from that list, you MUST use your `scouting_assistant` tool
            to perform a Google Search for the latest news, injury updates, or potential role changes.
        4.  Synthesize the player rankings with the real-time information you have gathered.
        5.  Provide a ranked list of your final recommendations, including a clear rationale for each
            that is grounded in the latest news you found.
        """,
        tools=[
            scout_tool,
            scout_agent.get_waiver_wire_players,
            scout_agent.get_my_roster,
            scout_agent.get_user_id,
        ],
    )
