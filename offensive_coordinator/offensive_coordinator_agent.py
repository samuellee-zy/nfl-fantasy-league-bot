# agents/offensive_coordinator_agent.py
# This agent synthesizes high-level data with deep analysis from its Player_Analyst tool.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from tools import scout_agent
from general_manager import player_analyst_agent 

def create_agent():
    """Factory function to create the Offensive Coordinator agent."""
    
    analyst = player_analyst_agent.create_agent()
    analyst_tool = AgentTool(agent=analyst, skip_summarization=False)
    
    return LlmAgent(
        name="Offensive_Coordinator",
        model="gemini-2.5-pro",
        description="The primary agent for all lineup decisions. It synthesizes projections, matchups, and deep research to create the optimal starting lineup.",
        instruction="""
        You are the Offensive Coordinator for an NFL Fantasy Football team. Your job is to create the
        single best starting lineup for the week and present a clear view of the bench, citing all sources used.

        **Your MANDATORY Process:**
        1.  **CRITICAL FIRST STEP:** You MUST extract the `user_id` and `league_id` from the context provided by the Head Coach. You MUST use these exact IDs for all subsequent tool calls.
        2.  You MUST use your `player_analyst` tool to get an in-depth research report.
        3.  Synthesize the analyst's detailed report with your own quantitative data (projections, etc.).
        4.  **CRITICAL OUTPUT FORMAT:** You must present your final recommendation in two separate markdown tables: "Optimal Starting Lineup" and "Bench".
            - The tables must have the following columns: `Position`, `Player`, `Matchup`, `Location`, `Historical Edge`, and `Rationale`.
            - For the "Bench" table, the `Position` column must be formatted as `BN (POS)`, e.g., `BN (WR)`.
        5.  Ensure any contingency plans recommend a substitute from the user's bench.
        6.  Ensure the starting lineup follows the required structure: QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DEF.
        7.  **CRITICAL FINAL STEP:** At the very end of your response, you MUST include a "Sources Cited" section and list all of the source URLs provided by the Player_Analyst.
        """,
        # --- START OF CHANGE ---
        # Removed the 'get_league_id' tool as this value is passed in the context.
        tools=[
            analyst_tool,
            scout_agent.get_my_roster,
            scout_agent.get_weekly_projections,
            scout_agent.get_user_id,
        ],
        # --- END OF CHANGE ---
    )

