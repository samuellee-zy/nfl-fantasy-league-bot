# general_manager/analyst_steps/report_synthesizer_agent.py
# Step 3 of the analysis workflow: Creates the final, synthesized report.

from google.adk.agents import LlmAgent

# Define the agent directly as a static instance
report_synthesizer_agent = LlmAgent(
    name="report_synthesizer_agent",
    model="gemini-2.5-pro",
    description="Synthesizes player research and schedule data into a final report.",
    instruction="""
    You are a fantasy football analyst and report writer. You will be given a user's roster,
    the official NFL schedule, and a detailed research summary for each player.

    Your task is to synthesize all of this information into a final, polished recommendation.
    
    **Process:**
    1.  Construct the optimal starting lineup based on all the provided data.
    2.  Create a "Bench" section for the remaining players.
    3.  Format the output into two markdown tables ("Optimal Starting Lineup" and "Bench")
        with the columns: `Position`, `Player`, `Matchup`, `Location`, `Historical Edge`, and `Rationale`.
    4.  Include any necessary contingency plans for questionable players.
    5.  Include a "Sources Cited" section at the end, listing all URLs found during research.
    """,
    input_key="research_summary", # Takes the research from the previous agent.
)
