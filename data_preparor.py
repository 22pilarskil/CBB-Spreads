import os
import json
import shutil

def sort_truncate_and_calculate_diff(data):
    home_team = next(filter(lambda x: x["home"], data), None)
    away_team = next(filter(lambda x: not x["home"], data), None)
    home_stats = home_team["stats"]
    away_stats = away_team["stats"]

    stats_diff = {}
    
    min_length = min(len(home_stats), len(away_stats))
    
    stats_keys = next(iter(home_stats.values())).keys()
    
    for key in stats_keys:
        home_sorted_values = sorted(
            [player[key] for player in home_stats.values()], reverse=True
        )[:min_length]
        away_sorted_values = sorted(
            [player[key] for player in away_stats.values()], reverse=True
        )[:min_length]
        
        diff_values = [home - away for home, away in zip(home_sorted_values, away_sorted_values)]
        stats_diff[key] = diff_values

    score_diff = home_team["score"] - away_team["score"]

    return {"team_diff": f"{home_team['team']} vs {away_team['team']}", "sorted_stats_diff": stats_diff, "score_diff": score_diff}

def process_directory(dataset_dir):

    output_dir = dataset_dir + "_diff"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".json"):

            with open(os.path.join(dataset_dir, filename), 'r') as file:
                data = json.load(file)

            sorted_stats = sort_truncate_and_calculate_diff(data)
            
            output_filename = os.path.splitext(filename)[0] + "_diff.json"
            with open(os.path.join(output_dir, output_filename), 'w') as file:
                json.dump(sorted_stats, file, indent=4)

if __name__ == '__main__':
    dataset = "dataset_womens"
    process_directory(dataset)
