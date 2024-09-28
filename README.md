# Bot Installation Guide

## Introduction

This bot gathers player statistics, sends broadcast messages, and uses an RCON-API integration to communicate with players. Follow the steps below to install and run the bot.

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

```
bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Setup a virtual Environment (Optional)
It is recommended to use a virtual environment to manage dependencies:
```
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### 3. Install Required Packages
Install the required Python packages using pip:
```
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
Create a .env file in the root directory with the following content:
```
API_TOKEN=your_api_token_here
BASE_URL=https://your-api-base-url.com
LOGGING_ENABLED=true
```
Replace your_api_token_here with your actual API token and https://your-api-base-url.com with the correct URL for your server.
### 5. Configure the broadcast.json File
Make sure the broadcast.json file contains valid broadcast messages. This file is used to send pre-set messages through the bot. Modify the file as needed:
```
[
    {
        "content": "Welcome to the battlefield!"
    },
    {
        "content": "Top players are being ranked now!"
    }
]
```
### 6. Run the Bot
Start the bot using the following command:
```
python bot.py
```
### 7. Usage
The bot will now:

- Fetch player statistics from the API.
- Send regular broadcast messages.
- Rank players in various categories (kills, defense, etc.).
### 8. Logging
If logging is enabled, you will see log messages printed to the console. To enable/disable logging, modify the LOGGING_ENABLED variable in the .env file.
### Troubleshooting
- Error accessing API: Check if the API_TOKEN and BASE_URL are correct in the .env file.
- No player data: Ensure the server is running and accessible via the API.
- Module not found: Ensure all dependencies are installed using the command pip install -r requirements.txt.
