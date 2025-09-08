# agents/schedule_agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import datetime

def create_agent():
    """Factory function to create the Schedule agent."""
    
    current_date = datetime.date.today().strftime("%B %d, %Y")
    # This correctly determines the current year is 2025
    current_year = datetime.date.today().year

    return LlmAgent(
        name="schedule_agent",
        model="gemini-2.5-pro", 
        description="An expert at finding the official NFL game schedule for a given week and season by cross-referencing multiple sources.",
        # --- START OF CHANGE ---
        # The instruction is updated to be more forceful about using the correct year.
        instruction=f"""
        You are a specialized research agent. Your sole purpose is to find and return the official NFL game schedule.
        Today's date is {current_date}.

        **Your MANDATORY Process:**
        1.  Based on today's date, the correct NFL season to use is **{current_year}**. You MUST IGNORE any other season year that may have been passed in from a previous step and use **{current_year}**.
        2.  Use the `Google Search` tool to find the official NFL schedule for the requested week of the **{current_year}** season.
        3.  Verify the schedule by cross-referencing at least two reputable sources (e.g., ESPN, NFL.com, CBS Sports). This is critical to ensure accuracy.
        4.  For each game, you must extract the away team, the home team, and the game's location.
        5.  You MUST return the final, verified schedule as a structured list of games. Do not add any conversational text or summaries, only the list.

        **Example of a correctly formatted response:**
        [
            {{"away_team": "Dallas Cowboys", "home_team": "Cleveland Browns", "location": "Cleveland, OH"}},
            {{"away_team": "Green Bay Packers", "home_team": "Philadelphia Eagles", "location": "São Paulo, Brazil"}}
        ]
        """,
        # --- END OF CHANGE ---
        tools=[google_search],
    )