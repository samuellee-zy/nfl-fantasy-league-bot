# agents/player_analyst_agent.py
# Defines the agent responsible for in-depth player research and lineup recommendations.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from tools import scout_agent
from general_manager import scouting_assistant_agent, schedule_agent

def create_agent():
    """Factory function to create the Player Analyst agent."""
    
    scout = scouting_assistant_agent.create_agent()
    scout_tool = AgentTool(agent=scout)
    
    schedule = schedule_agent.create_agent()
    schedule_tool = AgentTool(agent=schedule)

    return LlmAgent(
        name="player_analyst",
        model="gemini-2.5-pro",
        description="Performs deep-dive research on players by analyzing historical performance and delegating news gathering to a scouting assistant tool.",
        # **CHANGE**: Instructions updated to act on context from the parent agent.
        instruction="""
        You are an expert fantasy football analyst. Your goal is to provide a detailed, accurate report grounded in verified, real-time information.

        **Your MANDATORY Process:**
        1.  You will receive a task from your superior that includes the specific `season_year` and `week_number` to analyze, along with the user's `user_id` and `league_id`.
        2.  **Get Schedule:** You MUST use the `schedule_agent` tool to get the official NFL schedule for the season and week you were given.
        3.  **VERIFY SCHEDULE:** After receiving the schedule, you MUST perform a verification step. Use your `scouting_assistant` tool to search for one or two of the games from the list you received (e.g., "Cowboys vs Browns week 1 2025") to confirm the schedule data is accurate. Do not proceed if the schedule is incorrect.
        4.  **Get Roster:** Once the schedule is verified, use the `get_my_roster` tool with the correct user and league IDs.
        5.  **Research Players:** For each key player on the roster, perform research using their verified matchup.
            a. Use your `scouting_assistant` tool to find the latest news and injury updates from at least two reputable sources.
            b. Use `get_player_historical_stats` for past season performance.
        6.  Synthesize all verified information into a comprehensive report for the Offensive Coordinator, including a list of your sources.
        """,
        tools=[
            schedule_tool,
            scout_tool,
            scout_agent.get_my_roster,
            scout_agent.get_player_historical_stats,
        ],
    )

