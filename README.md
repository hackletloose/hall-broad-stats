# Bot Installation Guide

## Introduction

This bot gathers player statistics, sends broadcast messages, and uses an RCON-API integration to communicate with players. The bot now loads broadcast messages from a TXT file and sends them based on the specified interval. Follow the steps below to install and run the bot.

## ToDo:
Execute the following commands after downloading:
1. Copy the `.env.dist` file to `.env` and enter your values.
2. Run the command `pip install python-dotenv`.
3. Copy `broad-stats.service.dist` to `/etc/systemd/system/broad-stats.service`
4. Activate and start the service with `sudo systemctl enable broad-stats.service` and `sudo systemctl start broad-stats.service`.

## Prerequisites

Before installing the bot, make sure you have the following:

- **Python 3.8+** installed
- **pip** (Python package installer)
- A valid **API token** for the bot's integration
- Access to the **RCON API** for your game server
- **Git** installed on your machine

## Installation Steps

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/hackletloose/hall-braod-stats.git
cd hall-broad-stats
```

### 2. Setup a virtual Environment (Optional)

It is recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Required Packages

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```bash
API_TOKEN=your_api_token_here
BASE_URL=https://your-api-base-url.com
LOGGING_ENABLED=true
MESSAGE_FILE=messages.txt
```

Replace `your_api_token_here` with your actual API token, and `https://your-api-base-url.com` with the correct URL for your server. The `MESSAGE_FILE` points to the text file containing broadcast messages.

### 5. Configure the `messages.txt` File

The `messages.txt` file is used to send pre-set messages through the bot. Each line in the file should have the format:

```
<time_in_seconds> <message>
```

For example:

```
7 Welcome to the server! Please follow the server rules.
60 Join our Discord for VIP access!
```

### 6. Run the Bot

Start the bot using the following command:

```bash
python broad-stats.py
```

### 7. Usage

The bot will now:

- Fetch player statistics from the API.
- Send regular broadcast messages based on the `messages.txt` file.
- Rank players in various categories (kills, defense, etc.).

### 8. Logging

If logging is enabled, you will see log messages printed to the console. To enable/disable logging, modify the `LOGGING_ENABLED` variable in the `.env` file.

### Troubleshooting

- **Error accessing API**: Check if the `API_TOKEN` and `BASE_URL` are correct in the `.env` file.
- **No player data**: Ensure the server is running and accessible via the API.
- **Module not found**: Ensure all dependencies are installed using the command `pip install -r requirements.txt`.

