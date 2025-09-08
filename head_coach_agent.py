# agents/head_coach_agent.py
# Defines the parent agent (Head Coach) that coordinates the specialist agents.

from ADK.nfl_fantasy_league.offensive_coordinator import offensive_coordinator_agent
from google.adk.agents import LlmAgent  # <-- CORRECTED: Using LlmAgent is the proper way
from general_manager import general_manager_agent

def create_agent(user_context: dict):
    """
    Factory function to create the Head Coach agent and its sub-agents.
    
    Args:
        user_context (dict): The user's specific data (username, league_id, etc.).
    """
    
    oc_agent = offensive_coordinator_agent.create_agent()
    gm_agent = general_manager_agent.create_agent()
    
    sub_agents = [oc_agent, gm_agent]
    
    dynamic_introduction = "\n".join([f"- **{agent.name}**: {agent.description}" for agent in sub_agents])
    
    # Using LlmAgent with the 'sub_agents' parameter makes it the orchestrator.
    return LlmAgent(
        name="Head_Coach",
        model="gemini-2.5-pro",
        instruction=f"""
        You are the Head Coach of an elite NFL Fantasy Football team.
        You are the primary interface for the team manager and your job is to delegate tasks to your staff.

        **Your First Task:** On your first turn, introduce yourself and your coaching staff:
        {dynamic_introduction}

        **Your Main Task:** For all subsequent requests, your job is to understand the user's intent and context.
        1.  First, parse the user's message to identify the specific `season_year` and `week_number` they are asking about. If they don't specify, use the defaults from the initial context.
        2.  Based on the user's request, delegate the core task to the appropriate assistant coach.
            - For player analysis, matchups, and roster suggestions, delegate to the `Offensive_Coordinator`.
            - For trades, waiver wire pickups, and long-term strategy, delegate to the `General_Manager`.
        3.  Ensure that you ask the user's username and league_id for Sleeper before proceeding
        
        Synthesize the final response from your assistants into a clear and helpful answer.
        
        
        """,
        sub_agents=sub_agents,
    )

# Initial Context for fallback: {user_context}