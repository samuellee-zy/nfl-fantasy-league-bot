# agents/analyst_steps/report_synthesizer_agent.py
# Step 3 of the analysis workflow: Creates the final report.

from google.adk.agents import LlmAgent

def create_agent():
    """Factory function to create the report synthesizer agent."""
    return LlmAgent(
        name="report_synthesizer_agent",
        model="gemini-2.5-pro",
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
        5.  Include a "Sources Cited" section at the end.
        """,
        # **FIX**: Removed the invalid 'input_key' argument. The SequentialAgent handles this automatically.
    )

