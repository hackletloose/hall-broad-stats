# Hall Broad Stats Bot

Dieser kleine Bot sammelt Spielerstatistiken und verschickt automatisch Nachrichten über die RCON-Schnittstelle deines Servers. Die Anleitung richtet sich an Einsteiger und führt Schritt für Schritt durch die Einrichtung.

## Voraussetzungen
- **Python 3.8 oder höher**
- **pip** zum Installieren der Abhängigkeiten
- Einen gültigen **API-Token** für die RCON-API
- Optional: **git** zum Klonen des Repositories

## Installation
1. **Repository klonen (optional)**
   ```bash
   git clone https://github.com/hackletloose/hall-braod-stats.git
   cd hall-broad-stats
   ```
2. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigurationsdatei anlegen**
   Kopiere `.env.dist` zu `.env` und trage dort deine eigenen Werte ein:
   ```
   API_TOKEN=DEIN_API_TOKEN
   BASE_URL=https://dein-server.example.com
   LOGGING_ENABLED=true
   MESSAGE_FILE=messages.txt
   ```
4. **Broadcast-Nachrichten anpassen**
   In der Datei `messages.txt` legst du fest, welche Nachrichten in welchen Abständen gesendet werden. Jede Zeile besteht aus Zeit in Sekunden und dem Text der Nachricht:
   ```
   60 Willkommen auf dem Server!
   ```

## Bot starten
Den Bot startest du einfach mit:
```bash
python broad-stats.py
```

## Automatischer Start (optional)
Für einen Dauerbetrieb kannst du den mitgelieferten systemd-Service nutzen. Kopiere die Datei `hall-broad-stats.service.dist` nach `/etc/systemd/system/hall-broad-stats.service`, passe den Pfad an und aktiviere den Dienst dann mit:
```bash
sudo systemctl enable hall-broad-stats.service
sudo systemctl start hall-broad-stats.service
```

## Häufige Probleme
- **Fehler beim API-Zugriff** – Prüfe `API_TOKEN` und `BASE_URL` in deiner `.env`.
- **Keine Spielerdaten** – Stelle sicher, dass der Server läuft und erreichbar ist.
- **Module nicht gefunden** – Führe `pip install -r requirements.txt` aus, um alle Abhängigkeiten zu installieren.

Viel Erfolg und viel Spaß mit dem Bot!
