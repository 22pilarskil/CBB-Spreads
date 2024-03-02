
# import pandas module  
import pandas as pd  
    
# making dataframe
teams_df = pd.read_csv("ncaam-march-mania-2021/MDataFiles_Stage1/MTeams.csv")
game_results_df = pd.read_csv("ncaam-march-mania-2021/MDataFiles_Stage1/MRegularSeasonCompactResults.csv")  
   
# output the dataframe 
# print(teams_df)

team_names = {}
elo_dict = {}
team_ids = teams_df["TeamID"]
for ind in teams_df.index:
    elo_dict[teams_df["TeamID"][ind]] = 1500
    team_names[teams_df["TeamID"][ind]] = teams_df["TeamName"][ind]

#print(elo_dict)

season = game_results_df["Season"][0]

season = 2019
#print(season)
#print(elo_dict)
for ind in game_results_df.index:
    if(game_results_df["Season"][ind] >= 2019):
        if game_results_df["Season"][ind] != season:
            season = game_results_df["Season"][ind]
            #print(season)
            for key in elo_dict:
                elo_dict[key] = (0.75 * elo_dict[key]) + (0.25 * 1505)
    
        winTeam = game_results_df["WTeamID"][ind]
        loseTeam = game_results_df["LTeamID"][ind]
        Ewin = 1/(1 + pow(10, (elo_dict[loseTeam] - elo_dict[winTeam])/400))
        Elose = 1/(1 + pow(10, (elo_dict[winTeam] - elo_dict[loseTeam])/400))
        WScore = game_results_df["WScore"][ind]
        LScore = game_results_df["LScore"][ind]
        margin = WScore - LScore
        elo_dif = elo_dict[winTeam] - elo_dict[loseTeam]
        k = 20*((pow((margin + 3), 0.8))/(7.5 + 0.006*elo_dif))
        #print(Ewin, Elose, k)
        #print(elo_dict[winTeam], elo_dict[loseTeam])
        elo_dict[winTeam] = elo_dict[winTeam] + k*(1 - Ewin)
        elo_dict[loseTeam] = elo_dict[loseTeam] + k*(0 - Elose)
    

sorted_elos = sorted(elo_dict.items(), key=lambda x:x[1])[::-1]
sorted_elos_list = list(map(list, sorted_elos))
for i in range(len(sorted_elos_list)):
   sorted_elos_list[i][0] = team_names[sorted_elos_list[i][0]]
   sorted_elos_list[i][1] = round(sorted_elos_list[i][1], 4)
print(*sorted_elos_list, sep = "\n")
