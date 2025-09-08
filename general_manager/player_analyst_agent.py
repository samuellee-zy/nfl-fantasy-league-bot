# general_manager/player_analyst_agent.py
# This agent orchestrates the sequential workflow for detailed player analysis.

from google.adk.agents import SequentialAgent

# Import the static agent instances that will serve as steps in the sequence.
# These are absolute imports, consistent with the project's structure.
from general_manager.analyst_steps.data_gathering_agent import data_gathering_agent
from general_manager.analyst_steps.player_research_agent import player_research_agent
from general_manager.analyst_steps.report_synthesizer_agent import report_synthesizer_agent

# Define the Player Analyst as a SequentialAgent.
# This is the best practice for ensuring a multi-step process runs in a specific,
# guaranteed order every time. It will execute the sub-agents sequentially.
player_analyst_agent = SequentialAgent(
    name="player_analyst",
    description=(
        "A sequential agent that performs a deep-dive analysis. "
        "It first gathers the NFL schedule, then researches each player on the roster, "
        "and finally synthesizes a comprehensive report."
    ),
    # The agents will run in this exact order:
    # 1. data_gathering_agent
    # 2. player_research_agent
    # 3. report_synthesizer_agent
    sub_agents=[
        data_gathering_agent,
        player_research_agent,
        report_synthesizer_agent,
    ],
)

