# offensive_coordinator/offensive_coordinator_agent.py
# This agent synthesizes high-level data with deep analysis from its Player_Analyst tool.

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from ..tools import scout_agent
# Import the static player_analyst_agent instance
from ..general_manager.player_analyst_agent import player_analyst_agent

# Wrap the imported agent in a tool
analyst_tool = AgentTool(agent=player_analyst_agent, skip_summarization=False)

# Define the agent directly as a static instance
offensive_coordinator_agent = LlmAgent(
    name="Offensive_Coordinator",
    model="gemini-2.5-pro",
    description="The primary agent for all lineup decisions. It synthesizes projections, matchups, and deep research to create the optimal starting lineup.",
    instruction="""
    You are the Offensive Coordinator for an NFL Fantasy Football team. Your job is to create the
    single best starting lineup for the week and present a clear view of the bench, citing all sources used.

    **Your MANDATORY Process:**
    1.  **CRITICAL FIRST STEP:** You will receive the `user_id` and `league_id` from the Head Coach. You MUST use these exact IDs for all subsequent tool calls.
    2.  Use the `get_roster`, `get_weekly_projections`, and the `get_fantasy_matchups` tools to gather the necessary data.
    3.  You MUST use your `player_analyst` tool to get an in-depth research report.
    4.  Synthesize the analyst's detailed report, projection data, and specific fantasy matchup information to construct the best lineup.
    5.  **CRITICAL OUTPUT FORMAT:** You must present your final recommendation in two separate markdown tables: "Optimal Starting Lineup" and "Bench".
        - The tables must have the following columns: `Position`, `Player`, `Matchup`, `Location`, `Historical Edge`, and `Rationale`.
        - For the "Bench" table, the `Position` column must be formatted as `BN (POS)`, e.g., `BN (WR)`.
    6.  Ensure the starting lineup follows the required structure: QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DEF.
    7.  **CRITICAL FINAL STEP:** At the very end of your response, you MUST include a "Sources Cited" section and list all of the source URLs provided by the Player_Analyst.
    """,
    tools=[
        analyst_tool,
        scout_agent.get_roster,
        scout_agent.get_weekly_projections,
        scout_agent.get_user_id,
        scout_agent.get_fantasy_matchups,
    ],
)

