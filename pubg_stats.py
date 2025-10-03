import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
PUBG_API_KEY = os.getenv("PUBG_API_KEY")

# STEP 1: Get Player Info (to obtain player ID)
def get_player_info(player_name: str, api_key: str, platform_region: str = "steam") -> dict:
    """
    STEP 1: Fetches a player's basic account information, primarily their ID.
    """
    endpoint = f"https://api.pubg.com/shards/{platform_region}/players"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    params = {"filter[playerNames]": player_name}
    
    try:
        resp = requests.get(endpoint, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        if data['data']:
            player_info = {
                "id": data['data'][0]['id'],
                "name": data['data'][0]['attributes']['name'],
                "shardId": data['data'][0]['attributes']['shardId'],
            }
            return player_info
        else:
            return {"error": "Player not found"}
    except requests.exceptions.HTTPError as err:
        return {"error": f"HTTP Error: {err.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {e}"}


# STEP 2: Get Player Lifetime Stats
def get_player_lifetime_stats(player_id: str, api_key: str, platform_region: str = "steam") -> dict:
    """
    STEP 2: Fetches a player's lifetime stats using their account ID.
    """
    endpoint = f"https://api.pubg.com/shards/{platform_region}/players/{player_id}/seasons/lifetime"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    
    try:
        resp = requests.get(endpoint, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        
        # The stats are nested under game modes (solo, duo, squad, etc.)
        lifetime_stats = data['data']['attributes']['gameModeStats']
        return lifetime_stats
        
    except requests.exceptions.HTTPError as err:
        return {"error": f"HTTP Error: {err.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {e}"}


# Combined function
def get_pubg_data(player_name):
    # --- STEP 1: Get the Player ID ---
    player_account_info = get_player_info(player_name, PUBG_API_KEY)
    if "error" in player_account_info:
        print(f"An error occurred: {player_account_info['error']}")
    else:
        player_id = player_account_info['id']
        # --- STEP 2: Use the ID to get Lifetime Stats ---
        stats = get_player_lifetime_stats(player_id, PUBG_API_KEY)

        if "error" in stats:
            print(f"An error occurred while fetching stats: {stats['error']}")
        else:
            return stats["squad-fpp"]  # Example: return squad first-person stats

'''
if __name__ == "__main__":
    player_name = "Ots_Numb_"
    stats = get_pubg_data(player_name)
    # print(json.dumps(stats, indent=4))
    print(stats)
'''
    