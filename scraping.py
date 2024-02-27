from requestor import get
import pickle
import re
import json

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


def get_player_stats(input_str):

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


if __name__ == '__main__':
    print(get_ids()["Georgia Tech Yellow Jackets"])