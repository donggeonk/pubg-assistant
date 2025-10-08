import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from pubg_stats import get_player_info, get_player_lifetime_stats

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_player_lifetime_stat",
    "description": "Get the current PUBG player statistics for each mode (solo, duo, squad, and FPP variants), including: kills, assists, dailyKills, weeklyKills, wins, dailyWins, weeklyWins, losses, roundsPlayed, top10s, damageDealt, longestKill (meters), headshotKills, maxKillStreaks, roundMostKills, suicides, dBNOs, revives, teamKills, roadKills, vehicleDestroys, walkDistance (meters), rideDistance (meters), swimDistance (meters), timeSurvived (seconds), longestTimeSurvived (seconds), mostSurvivalTime (seconds), heals, boosts, weaponsAcquired, winPoints (points), killPoints (points), rankPoints (points), rankPointsTitle (string), and days.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],
    },
}]

user_input = input("User: ")
# instructions tell the AI that it can call a function to get the weather
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "You can call a function to get the weather."}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool
    functions=functions,
    function_call="auto",
)

message = response.choices[0].message
print("First LLM response:", message)

# If it decided to call get_weather:
if message.function_call:
    args = json.loads(message.function_call.arguments)
    print("Arguments of get_weather:", args)
    temp = get_weather(**args)
    print("Temperature from get_weather:", temp)

    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the current weather in the city."},
        {"role": "user",   "content": user_input},
        message,
        {
            "role": "function",
            "name": message.function_call.name,
            "content": json.dumps({ "temperature": temp })
        }
    ]

    # send the function call result back to the LLM so it can generate a followup response
    followup = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=followup_messages,
    )
    print("Bot:", followup.choices[0].message.content)
else:
    # otherwise it answered directly or didn't call a function
    print("Bot:", message.content)


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
            return stats


if __name__ == "__main__":
    player_name = "Scout"
    stats = get_pubg_data(player_name)
    print(json.dumps(stats, indent=4))