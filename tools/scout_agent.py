# agents/scout_agent.py
# This file contains all the data-gathering functions (tools) that
# connect to the Sleeper API and scrape the web for real-world data.

import os
import time
import json
import requests
from bs4 import BeautifulSoup

# --- Data Caching and Loading ---

def get_all_players_data():
    """
    Fetches a comprehensive list of all NFL players from the Sleeper API.
    To optimize performance, this data is cached locally in a players.json file.
    The cache is updated once every 24 hours.
    
    Returns:
        dict: A dictionary where keys are player IDs and values are player data objects.
    """
    cache_file = 'players.json'
    cache_duration_seconds = 24 * 60 * 60  # 24 hours

    if os.path.exists(cache_file):
        file_mod_time = os.path.getmtime(cache_file)
        if (time.time() - file_mod_time) < cache_duration_seconds:
            print("Loading players data from local cache...")
            with open(cache_file, 'r') as f:
                return json.load(f)

    print("Fetching all players data from Sleeper API...")
    url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        players_data = response.json()
        with open(cache_file, 'w') as f:
            json.dump(players_data, f)
        return players_data
    else:
        print(f"Error fetching players data: Status code {response.status_code}")
        return None

# --- API Tool Functions ---

ALL_PLAYERS = get_all_players_data()

def get_user_id(username: str) -> str | None:
    """
    Fetches the user ID for a given Sleeper username.

    Args:
        username (str): The Sleeper username.

    Returns:
        str | None: The user's unique ID, or None if not found.
    """
    url = f"https://api.sleeper.app/v1/user/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            if user_data and 'user_id' in user_data:
                return user_data['user_id']
        print(f"Error fetching user ID for {username}: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching user ID: {e}")
    return None


def get_roster(league_id: str, user_id: str) -> list[dict]:
    """
    Fetches the user's current roster for a specific fantasy league.

    Args:
        league_id (str): The unique identifier for the Sleeper league.
        user_id (str): The user's unique identifier.

    Returns:
        list[dict]: A list of player objects on the user's roster, or an empty list on failure.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            rosters = response.json()
            if rosters:
                for roster in rosters:
                    if roster.get('owner_id') == user_id:
                        player_ids = roster.get('players', [])
                        roster_details = [ALL_PLAYERS.get(pid) for pid in player_ids if ALL_PLAYERS.get(pid)]
                        return roster_details
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching roster: {e}")
    return []

def get_waiver_wire_players(league_id: str, limit: int = 10) -> list[dict]:
    """
    Identifies the top available players on the waiver wire for a given league.
    It filters out retired players and non-offensive positions.

    Args:
        league_id (str): The unique identifier for the Sleeper league.
        limit (int): The maximum number of players to return. Defaults to 10.

    Returns:
        list[dict]: A list of top available players, or an empty list on failure.
    """
    rosters_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    try:
        rosters_response = requests.get(rosters_url)
        if rosters_response.status_code != 200:
            return []
        
        rosters_data = rosters_response.json()
        if not rosters_data:
            return []

        rostered_player_ids = set()
        for roster in rosters_data:
            for player_id in roster.get('players', []):
                rostered_player_ids.add(player_id)

        free_agents = []
        offensive_positions = {'QB', 'RB', 'WR', 'TE'}
        for player_id, player_data in ALL_PLAYERS.items():
            if player_id not in rostered_player_ids and player_data.get('active'):
                if player_data.get('position') in offensive_positions:
                    free_agents.append(player_data)

        free_agents.sort(key=lambda p: p.get('search_rank') if p.get('search_rank') is not None else 9999)
        return free_agents[:limit]
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching waiver wire players: {e}")
    return []


def get_weekly_projections(week: int) -> dict:
    """
    Fetches fantasy projections for all players for a specific week.

    Args:
        week (int): The NFL week number.

    Returns:
        dict: A dictionary of player projections, or an empty dict on failure.
    """

    url = f"https://api.sleeper.app/v1/projections/nfl/regular/{week}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching projections: {e}")
    return {}

def get_player_historical_stats(player_id: str, season: int) -> dict:
    """
    Fetches a single player's fantasy football stats for an entire past season.

    Args:
        player_id (str): The unique identifier for the player.
        season (int): The year of the season to fetch (e.g., 2023).

    Returns:
        dict: An object containing the player's stats for that season, or an empty dict if not found.
    """
    url = f"https://api.sleeper.app/v1/stats/nfl/regular/{season}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            season_stats = response.json()
            if season_stats and player_id in season_stats:
                return season_stats[player_id]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching historical stats: {e}")
    return {}

def get_fantasy_matchups(league_id: str, week: int) -> list[dict]:
    """
    Fetches the specific fantasy matchups for a given league and week from the Sleeper API.

    Args:
        league_id (str): The unique identifier for the Sleeper league.
        week (int): The NFL week number.

    Returns:
        list[dict]: A list of matchup objects, including roster and opponent info.
                    Returns an empty list on failure.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching fantasy matchups: {e}")
    return []
