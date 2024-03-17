import requests
import json


api_key = "3db1720406be4e95833ba365a9e9c670"

headers = {
    'Ocp-Apim-Subscription-Key': api_key
}

def get_player_season_stats(season="2018"):
    url = f"https://api.sportsdata.io/v3/cbb/stats/json/PlayerSeasonStats/{season}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open(f'player_season_stats_{season}.json', 'w') as json_file:
            json.dump(data, json_file)

def load_player_season_stats(season="2018"):
    with open(f'player_season_stats_{season}.json', 'r') as json_file:
        return json.load(json_file)

def get_player_game_stats(date="2018-FEB-27"):
    url = f"https://api.sportsdata.io/v3/cbb/stats/json/PlayerGameStatsByDate/{date}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open(f'player_game_stats_{date}.json', 'w') as json_file:
            json.dump(data, json_file)

def load_player_season_stats(season="2018-FEB-27"):
    with open(f'player_game_stats_{season}.json', 'r') as json_file:
        return json.load(json_file)


# get_player_season_stats()
data = load_player_season_stats()
print(len(data))
print(data[1])