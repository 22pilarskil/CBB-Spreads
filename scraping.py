from requestor import get
import pickle
import re
import json
from datetime import datetime, timedelta
import os
import threading
import schedule
import time

html_content = "Placeholder for HTML content from the URL: https://www.espn.com/mens-college-basketball/teams"

# Save the HTML content to a text file
file_path = "espn_mens_college_basketball_teams.html"

# with open(file_path, "w") as file:
#     file.write(get("https://www.espn.com/mens-college-basketball/teams").text)


def scrape_ids(file_path="ids.json"):

    id_str = get("https://www.espn.com/mens-college-basketball/teams").text
    matches = re.findall(r'\{"n":(.*?)\}\]\}', id_str, re.DOTALL) 
    ids = {}
    for match in matches:
        json_obj = json.loads('{"n":' + match + '}]}')
        ids[json_obj["n"]] = json_obj["id"]
    with open(file_path, "w") as file:
        json.dump(ids, file)


def get_ids(file_path="ids.json"):

    with open(file_path, "r") as file:
        return json.load(file)


def get_player_stats(id):

    input_str = get(f"https://www.espn.com/mens-college-basketball/team/stats/_/id/{id}").text
    match = re.search(r'"playerStats":\[\[(.*?)\]\]', input_str, re.DOTALL)
    if match:
        stats = {}
        json_stats = json.loads("[[" + match.group(1) + "]]")
        for i in range(len(json_stats[1])):
            stats.update(player_stats_parse_individual(json_stats[0][i]))
        return stats
    else:
        return "No match found"
    
    
def player_stats_parse_individual(data):

    player_name = data.get('athlete', {}).get('name', 'Unknown Player')
    concise_stats = {player_name: {}}
    
    for stat in data.get('statGroups', {}).get('stats', []):
        stat_name = stat.get('abbreviation', 'Unknown Stat')
        stat_value = stat.get('displayValue', 'N/A')
        
        try:
            stat_value = float(stat_value)
        except ValueError:
            pass
        
        concise_stats[player_name][stat_name] = stat_value
    
    return concise_stats


def daily_update():

    current_date = datetime.now()
    day_before = current_date - timedelta(days=1)
    formatted_date = day_before.strftime('%Y%m%d')
    print(formatted_date)

    html_content = get(f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{formatted_date}").text

    evts_index = html_content.find("evts")
    start_index = html_content.find("[", evts_index)

    if evts_index == -1 or start_index == -1: return None
    
    counter = 1
    i = start_index + 1 
    
    while i < len(html_content) and counter > 0:
        if html_content[i] == "[":
            counter += 1
        elif html_content[i] == "]":
            counter -= 1
        i += 1

    if counter == 0:
        end_index = i
        games = json.loads(html_content[start_index:end_index])
    else:
        return None
    
    dataset_dir = 'dataset'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    
    for game in games:
        for team in game['competitors']:
            if team.get('winner', False):  # Default to False if 'winner' key does not exist
                winning_team = team['displayName']
                winning_score = team['score']
                winner_home_status = team['isHome']
            else:
                losing_team = team['displayName']
                losing_score = team['score']
                loser_home_status = team['isHome']

        game_data = [{
                    "team":winning_team, 
                    "score":winning_score, 
                    "home":winner_home_status, 
                    "stats":get_player_stats(get_ids()[winning_team])
                }, {
                    "team":losing_team, 
                    "score":losing_score, 
                    "home":loser_home_status, 
                    "stats":get_player_stats(get_ids()[losing_team])
                }]
    
        fname = os.path.join(dataset_dir, f"{winning_team}-{losing_team}-{formatted_date}.json")
        print(f"Adding {fname}")
        with open(fname, "w+") as file:
            json.dump(game_data, file)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def schedule_daily_update():
    schedule.every().day.at("17:13").do(run_threaded, daily_update)

    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    schedule_daily_update()