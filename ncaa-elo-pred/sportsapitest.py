
import requests
import json
from datetime import date, timedelta
import pandas as pd    



def elocalcs(elo_dict, start_date, end_date):   
    #start_date = date(2023, 11, 6)
    #end_date = date(2023, 3, 8)
    delta = timedelta(days=1)
    while start_date <= end_date:
        curr_string_date = start_date.strftime("%Y-%m-%d")
        gameday_request=requests.get('https://api.sportsdata.io/v3/cbb/scores/json/ScoresBasic/' + curr_string_date + '?key=3602ceda845a46378cedb82ff348cad9')
        #print(start_date.strftime("%Y-%m-%d"))
        start_date += delta
        gameday_response_json = gameday_request.json()
        gameday_df = pd.json_normalize(gameday_response_json)
        if(gameday_df.empty):
            continue
        gameday_df = gameday_df.drop(gameday_df[gameday_df['Status'] == 'Canceled'].index)

        #print(gameday_df)

        for index, row in gameday_df.iterrows():
            winTeam = 0
            loseTeam = 0
            awayWin = False
            if row['AwayTeamScore'] > row['HomeTeamScore']:
                awayWin = True
                winTeam = row['AwayTeamID']
                loseTeam = row['HomeTeamID']
            else:
                winTeam = row['HomeTeamID']
                loseTeam = row['AwayTeamID']
            
            if winTeam == 0 or loseTeam == 0 or winTeam in elo_dict == False or loseTeam in elo_dict == False:
                break
            Ewin = 1/(1 + pow(10, (elo_dict[loseTeam] - elo_dict[winTeam])/400))
            Elose = 1/(1 + pow(10, (elo_dict[winTeam] - elo_dict[loseTeam])/400))
            WScore = 0
            LScore = 0
            if awayWin:
                WScore = row['AwayTeamScore']
                LScore = row['HomeTeamScore']
            else:
                WScore = row['HomeTeamScore']
                LScore = row['AwayTeamScore']
            margin = WScore - LScore
            elo_dif = elo_dict[winTeam] - elo_dict[loseTeam]
            k = 20*((pow((margin + 3), 0.8))/(7.5 + 0.006*elo_dif))
            #print(Ewin, Elose, k)
            #print(elo_dict[winTeam], elo_dict[loseTeam])
            elo_dict[winTeam] = elo_dict[winTeam] + k*(1 - Ewin)
            elo_dict[loseTeam] = elo_dict[loseTeam] + k*(0 - Elose)


    #print(elo_dict)

teams_request=requests.get('https://api.sportsdata.io/v3/cbb/scores/json/teams?key=3602ceda845a46378cedb82ff348cad9')
teams_response_json = teams_request.json()
teams_df = pd.json_normalize(teams_response_json)
#teams_df = teams_df.drop(teams_df[teams_df['Active'] == False].index)
print(teams_df)
elo_dict = {}
team_names = {}
for index, row in teams_df.iterrows():
    #print(row['TeamID'])
    elo_dict[row['TeamID']] = 1500
    team_names[row['TeamID']] = row['School']

elocalcs(elo_dict, date(2023, 11, 6), date(2024, 3, 8))

sorted_elos = sorted(elo_dict.items(), key=lambda x:x[1])[::-1]
sorted_elos_list = list(map(list, sorted_elos))
for i in range(len(sorted_elos_list)):
   sorted_elos_list[i][0] = team_names[sorted_elos_list[i][0]]
   sorted_elos_list[i][1] = round(sorted_elos_list[i][1], 4)
print(*sorted_elos_list, sep = "\n")

#print(elo_dict)

