# general_manager/analyst_steps/report_synthesizer_agent.py
# Step 3 of the analysis workflow: Creates the final, synthesized report.

from google.adk.agents import LlmAgent

# Define the agent directly as a static instance
report_synthesizer_agent = LlmAgent(
    name="report_synthesizer_agent",
    model="gemini-2.5-pro",
    description="Synthesizes player research and schedule data into a final report.",
    instruction="""
    You are a fantasy football analyst and report writer. Your input will be a single block of text
    from the previous step containing three sections: "NFL Schedule", "User Roster", and "Player Research Summary".

    Your task is to parse this input and synthesize all of the information into a final, polished recommendation.
    
    **Process:**
    1.  Extract the schedule, roster, and research summary from your input text.
    2.  Construct the optimal starting lineup based on all the provided data.
    3.  Create a "Bench" section for the remaining players.
    4.  Format the output into two markdown tables ("Optimal Starting Lineup" and "Bench")
        with the columns: `Position`, `Player`, `Matchup`, `Location`, `Historical Edge`, and `Rationale`.
    5.  Include any necessary contingency plans for questionable players.
    6.  Include a "Sources Cited" section at the end, listing all URLs found during research.
    """,
)

