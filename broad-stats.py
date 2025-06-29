import requests
import time
import random
import sys
from dotenv import load_dotenv
import os

load_dotenv()
api_token = os.getenv('API_TOKEN')
BASE_URL = os.getenv('BASE_URL')
LOGGING_ENABLED = os.getenv('LOGGING_ENABLED', 'false').lower() == 'true'

def log(message):
    if LOGGING_ENABLED:
        print(f"[LOG]: {message}")

def get_team_view(api_token):
    url = f"{BASE_URL}/api/get_team_view"
    headers = {"Authorization": f"Bearer {api_token}"}
    try:
        response = requests.get(url, headers=headers)
    except requests.RequestException as e:
        log(f"Request failed: {e}")
        return None
    if response.status_code == 200:
        team_view_data = response.json()
        if "allies" in team_view_data["result"] and "axis" in team_view_data["result"]:
            allies = team_view_data["result"]["allies"]["squads"]
            axis = team_view_data["result"]["axis"]["squads"]
            all_players = []
            for squad_name, squad in allies.items():
                for player in squad["players"]:
                    player_info = extract_player_info(player)
                    all_players.append(player_info)
            for squad_name, squad in axis.items():
                for player in squad["players"]:
                    player_info = extract_player_info(player)
                    all_players.append(player_info)
            return all_players
        else:
            log("No player data available.")
            return []
    else:
        log(f"Error accessing API: {response.status_code}")
        return None

def extract_player_info(player):
    return {
        "name": player["name"],
        "combat": player["combat"],
        "level": player["level"],
        "kills": player["kills"],
        "deaths": player["deaths"],
        "offense": player["offense"],
        "defense": player["defense"],
        "support": player["support"]
    }

def send_broadcast(api_token, message):
    api_data = {"message": message, "save": "True"}
    api_url = f"{BASE_URL}/api/set_broadcast"
    headers = {"Authorization": f"Bearer {api_token}"}
    try:
        response = requests.post(api_url, json=api_data, headers=headers)
    except requests.RequestException as e:
        log(f"Request failed: {e}")
        return False
    if response.status_code == 200:
        log(f"Data successfully sent to the API: {message}")
        return True
    else:
        log(f"Error sending data to the API. {response.status_code}")
        return False

def print_top_players(all_players, category_name, title):
    if not all_players or not all(isinstance(player, dict) for player in all_players):
        log(f"Invalid player data: {all_players}")
        return
    
    sorted_players = sorted(all_players, key=lambda x: x.get(category_name, 0), reverse=True)
    top_players_str = f"{title} "
    for idx, player in enumerate(sorted_players[:5], 1):
        player_name = player.get('name', 'unknown')
        player_stat = player.get(category_name, 'unknown')
        top_players_str += f"{idx}. {player_name} ({player_stat}),          "
    log(top_players_str.rstrip(" ____ "))
    send_broadcast(api_token, top_players_str.rstrip(" , ") + "          " + top_players_str.rstrip(" , ") + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , "))

def load_messages_from_txt(file_path):
    messages = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                time_value, message = line.split(' ', 1)
                messages.append((int(time_value), message.strip()))
    return messages

def main(api_token):
    file_path = 'messages.txt'
    messages = load_messages_from_txt(file_path)
    categories = ["kills", "level", "deaths", "offense", "defense", "support", "combat"]

    for time_value, message in messages:
        log(f"Sende Nachricht: {message}")
        send_broadcast(api_token, message)
        log(f"Wait {time_value} Seconds until the next message.")
        time.sleep(time_value)
        selected_category = random.choice(categories)
        all_players = get_team_view(api_token)
        if all_players:
            if selected_category == "kills":
                print_top_players(all_players, selected_category, f"Our top killing machines:          ")
            elif selected_category == "level":
                print_top_players(all_players, selected_category, f"Top levels on the server:          ")
            elif selected_category == "deaths":
                print_top_players(all_players, selected_category, f"Losers with the most deaths:          ")
            elif selected_category == "offense":
                print_top_players(all_players, selected_category, f"The best offensive:          ")
            elif selected_category == "defense":
                print_top_players(all_players, selected_category, f"The best defence:          ")
            elif selected_category == "support":
                print_top_players(all_players, selected_category, f"The best supporters:          ")
            else:
                print_top_players(all_players, selected_category, f"The best in combat:          ")
            countdown = 120
            while countdown > 0:
                sys.stdout.write(f"\rCountdown: {countdown} Seconds")
                sys.stdout.flush()
                time.sleep(1)
                countdown -= 1

if __name__ == "__main__":
    main(api_token)
