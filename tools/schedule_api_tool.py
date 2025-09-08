import requests
import json

def fetch_schedule_from_api(season_year: int = 2025, week: int = None) -> str:
    """
    Fetches the NFL schedule for a given season year and optional week from the ESPN API.

    Args:
        season_year: The year of the NFL season (e.g., 2025).
        week: The specific week to fetch. If None, fetches the entire season.

    Returns:
        A JSON string representing the list of games in the expected format.
        Returns an empty list as a string if the request fails.
    """
    base_url = f"http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    # The API uses season 'type' 2 for regular season weeks
    params = {
        "dates": season_year,
        "seasontype": 2,
    }
    
    if week:
        params["week"] = week

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        games = []
        for event in data.get("events", []):
            competition = event.get("competitions", [{}])[0]
            competitors = competition.get("competitors", [])
            venue = competition.get("venue", {})
            
            if len(competitors) == 2:
                home_team_data = next((c for c in competitors if c.get("homeAway") == "home"), {})
                away_team_data = next((c for c in competitors if c.get("homeAway") == "away"), {})

                game_info = {
                    "away_team": away_team_data.get("team", {}).get("displayName", "N/A"),
                    "home_team": home_team_data.get("team", {}).get("displayName", "N/A"),
                    "location": f"{venue.get('address', {}).get('city', 'N/A')}, {venue.get('address', {}).get('state', 'N/A')}"
                }
                games.append(game_info)
        
        # Return the data as a JSON string, which is standard for agent tools
        return json.dumps(games)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NFL schedule: {e}")
        return json.dumps([]) # Return an empty list on error
