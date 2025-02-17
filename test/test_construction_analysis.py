import sys
import os
import json
sys.path.append('../../')

from participant_analysis import construction_analysis, dir_path

#Utrecht
utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
utrecht_colors = ["#FF800E", "#5F9ED1", "#595959", "#ABABAB", "#006BA4"]
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_participants_d = json.load(infile)

construction_analysis(incident=utrecht_shooting,
                        data_d=utrecht_participants_d,
                        ordered_l=utrecht_ordered,
                        output_folder=dir_path,
                        colors=utrecht_colors,
                        verbose=1)

#mh17
mh17_ordered = ["0-1","2-7","8-15","19-130","318-806",
                "1084-1728"]
mh17 = "Q17374096"
mh17_colors = ["#595959", "#5F9ED1", "#ABABAB", "#FF800E", "#006BA4"]
with open(f"../output/{mh17}/participants_info.json", "r") as infile:
    mh17_participants_d = json.load(infile)

construction_analysis(incident=mh17,
                        data_d=mh17_participants_d,
                        ordered_l=mh17_ordered,
                        output_folder=dir_path,
                        colors=mh17_colors,
                        figsize=(10,5),
                        verbose=1)

#curfew riots
curfew_ordered = ["0-2", "3", "4-7"]
dutch_curfew_riots = "Q105077032"
curfew_colors = ["#ABABAB", "#5F9ED1", "#595959", "#FF800E", "#006BA4"]
with open(f"../output/{dutch_curfew_riots}/participants_info.json", "r") as infile:
    curfew_participants_d = json.load(infile)

construction_analysis(incident=dutch_curfew_riots,
                        data_d=curfew_participants_d,
                        ordered_l=curfew_ordered,
                        output_folder=dir_path,
                        colors=curfew_colors,
                        verbose=1)

#eurovision
eurovision_song_contest = "Q30973589"
eurovision_ordered = ["-730--620","-604--470","-465--424",
                      "-419--242","-90--28","-26--1","0-13"]
eurovision_colors = ["#5F9ED1", "#FF800E", "#ABABAB", "#595959", "#006BA4"]
with open(f"../output/{eurovision_song_contest}/participants_info.json", "r") as infile:
    eurovision_participants_d = json.load(infile)

construction_analysis(incident=eurovision_song_contest,
                        data_d=eurovision_participants_d,
                        ordered_l=eurovision_ordered,
                        output_folder=dir_path,
                        colors=eurovision_colors,
                        figsize=(10,5),
                        verbose=1)
