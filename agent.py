# main.py
# This file is the new entry point for the ADK command-line tool,
# defining the root agent for the application.

from google.adk.agents import LlmAgent

# Import the statically defined sub-agents using relative imports
from .offensive_coordinator.offensive_coordinator_agent import offensive_coordinator_agent
from .general_manager.general_manager_agent import general_manager_agent

# The sub_agents are instantiated in their own files and imported here.
sub_agents = [offensive_coordinator_agent, general_manager_agent]

# The introduction is now generated once, when the application starts.
dynamic_introduction = "\n".join(
    [f"- **{agent.name}**: {agent.description}" for agent in sub_agents]
)

# The root_agent is the main agent that the ADK server will interact with.
# In this architecture, it is the "Head_Coach".
root_agent = LlmAgent(
    name="Head_Coach",
    model="gemini-2.5-pro",
    instruction=f"""
    You are the Head Coach of an elite NFL Fantasy Football team.
    You are the primary interface for the team manager and your job is to delegate tasks to your staff.

    **Your First Task:** On your first turn, you MUST introduce yourself and your coaching staff. Then, you MUST ask the user for their Sleeper username and their Sleeper League ID. Do not proceed until you have this information.
    Coaching Staff:
    {dynamic_introduction}

    **Your Main Task:** For all subsequent requests, your job is to understand the user's intent.
    1.  First, parse the user's message to identify the specific `season_year` and `week_number` they are asking about.
    2.  Based on the user's request, delegate the core task to the appropriate assistant coach, making sure to pass them the `user_id` and `league_id` you have gathered.
        - For player analysis, matchups, and roster suggestions, delegate to the `Offensive_Coordinator`.
        - For trades, waiver wire pickups, and long-term strategy, delegate to the `General_Manager`.
    3.  Synthesize the final response from your assistants into a clear and helpful answer.
    """,
    sub_agents=sub_agents,
)

print("Root agent definition loaded successfully from main.py. Ready for ADK server.")

