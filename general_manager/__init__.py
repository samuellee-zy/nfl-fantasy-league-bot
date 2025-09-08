# # agents/__init__.py
# # This file makes the 'agents' folder a Python package and defines the
# # main entry point for the ADK command-line tool.

# from .. import head_coach_agent
# from tools import scout_agent
# import datetime

# # --- STATIC USER CONTEXT ---
# # **CHANGE**: This context is now static. The agents will be instructed
# # to get the dynamic week/season from the user's chat prompt.

# # Stored user information
# SLEEPER_USERNAME = "lemonsgiveslife"
# LEAGUE_ID = "1267611115785924608"

# print(f"Fetching user ID for {SLEEPER_USERNAME}...")
# user_id = scout_agent.get_user_id(SLEEPER_USERNAME)

# if not user_id:
#     print(f"FATAL: Could not find user ID for username '{SLEEPER_USERNAME}'. Exiting.")
#     exit()

# print(f"Successfully found user ID: {user_id}")

# USER_CONTEXT = {
#     "username": SLEEPER_USERNAME,
#     "league_id": LEAGUE_ID,
#     "user_id": user_id,
#     # Provide default fallback values
#     "season_year": datetime.date.today().year,
#     "week_number": 1
# }

# # Create the root agent and inject the context.
# root_agent = head_coach_agent.create_agent(user_context=USER_CONTEXT)

# print("Agent definition loaded from 'agents' package. Ready for ADK server.")

