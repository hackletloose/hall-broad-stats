import json
import requests
import time
import random
import sys
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# Umgebungsvariablen abrufen
api_token = os.getenv('API_TOKEN')
BASE_URL = os.getenv('BASE_URL')
LOGGING_ENABLED = os.getenv('LOGGING_ENABLED', 'false').lower() == 'true'

# JSON-Daten laden
with open('broadcast.json', 'r') as json_file:
    json_data = json.load(json_file)

def log(message):
    if LOGGING_ENABLED:
        print(f"[LOG]: {message}")

def get_team_view(api_token):
    url = f"{BASE_URL}/api/get_team_view"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        team_view_data = response.json()
        # Überprüfung hinzugefügt, ob Spielerdaten vorhanden sind
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
            log("Keine Spielerdaten verfügbar.")
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
    response = requests.post(api_url, json=api_data, headers=headers)
    if response.status_code == 200:
        log(f"Daten erfolgreich an die API gesendet: {message}")
    else:
        log(f"Fehler beim Senden der Daten an die API: {response.status_code}")

def print_top_players(all_players, category_name, title):
    if not all_players or not all(isinstance(player, dict) for player in all_players):
        log(f"Ungültige Spielerdaten: {all_players}")
        return
    
    sorted_players = sorted(all_players, key=lambda x: x.get(category_name, 0), reverse=True)
    top_players_str = f"{title} "
    for idx, player in enumerate(sorted_players[:5], 1):
        player_name = player.get('name', 'Unbekannt')
        player_stat = player.get(category_name, 'Unbekannt')
        top_players_str += f"{idx}. {player_name} ({player_stat}),          "
    log(top_players_str.rstrip(" ____ "))
    send_broadcast(api_token, top_players_str.rstrip(" , ") + "          " + top_players_str.rstrip(" , ") + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , ")  + "          " + top_players_str.rstrip(" , "))

def main(api_token):
    json_index = 0
    categories = ["kills", "level", "deaths", "offense", "defense", "support", "combat"]
    while True:
        # Nachricht aus Spielerstatistiken senden
        selected_category = "kills"
        all_players = get_team_view(api_token)
        print_top_players(all_players, selected_category, f"Unser TOP-Killermaschinen:          ")
        countdown = 120
        while countdown > 0:
            sys.stdout.write(f"\rCountdown: {countdown} Sekunden")
            sys.stdout.flush()
            time.sleep(1)
            countdown -= 1

        # Nachricht aus JSON senden
        send_broadcast(api_token, json_data[json_index]["content"])
        json_index = (json_index + 1) % len(json_data)
        # Countdown
        countdown = 120
        while countdown > 0:
            sys.stdout.write(f"\rCountdown: {countdown} Sekunden")
            sys.stdout.flush()
            time.sleep(1)
            countdown -= 1

        selected_category = random.choice(categories)
        all_players = get_team_view(api_token)
        if all_players:
            if selected_category == "kills":
                print_top_players(all_players, selected_category, f"Unser TOP-Killermaschinen:          ")
            elif selected_category == "level":
                print_top_players(all_players, selected_category, f"TOP-Levels auf dem Server:          ")
            elif selected_category == "deaths":
                print_top_players(all_players, selected_category, f"Versager mit den meisten Toden:          ")
            elif selected_category == "offense":
                print_top_players(all_players, selected_category, f"Die beste Offensive:          ")
            elif selected_category == "defense":
                print_top_players(all_players, selected_category, f"Die beste Defense:          ")
            elif selected_category == "support":
                print_top_players(all_players, selected_category, f"Der beste Support:          ")
            else:
                print_top_players(all_players, selected_category, f"Die bestem im Gefecht:          ")
            countdown = 120
            while countdown > 0:
                sys.stdout.write(f"\rCountdown: {countdown} Sekunden")
                sys.stdout.flush()
                time.sleep(1)
                countdown -= 1

if __name__ == "__main__":
    main(api_token)
