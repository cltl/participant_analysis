import sys
import os
import json
sys.path.append('../../')

from participant_analysis import fe_analysis, dir_path

#Utrecht
utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_participants_d = json.load(infile)

fe_analysis(incident=utrecht_shooting,
            data_dict=utrecht_participants_d,
            ordered_time_buckets=utrecht_ordered,
            output_folder=dir_path,
            dimension="frame elements",
            verbose=2)

#mh17
mh17_ordered = ["0-1","2-7","8-15","19-130","318-806",
                "1084-1728"]
mh17 = "Q17374096"
with open(f"../output/{mh17}/participants_info.json", "r") as infile:
    mh17_participants_d = json.load(infile)

fe_analysis(incident=mh17,
            data_dict=mh17_participants_d,
            ordered_time_buckets=mh17_ordered,
            output_folder=dir_path,
            dimension="frame elements",
            verbose=2)

#curfew riots
curfew_ordered = ["0-2", "3", "4-7"]
dutch_curfew_riots = "Q105077032"
with open(f"../output/{dutch_curfew_riots}/participants_info.json", "r") as infile:
    curfew_participants_d = json.load(infile)

fe_analysis(incident=dutch_curfew_riots,
            data_dict=curfew_participants_d,
            ordered_time_buckets=curfew_ordered,
            output_folder=dir_path,
            dimension="frame elements",
            verbose=2)

#eurovision
eurovision_song_contest = "Q30973589"
eurovision_ordered = ["-730--620","-604--470","-465--424",
                      "-419--242","-90--28","-26--1","0-13"]
with open(f"../output/{eurovision_song_contest}/participants_info.json", "r") as infile:
    eurovision_participants_d = json.load(infile)

fe_analysis(incident=eurovision_song_contest,
            data_dict=eurovision_participants_d,
            ordered_time_buckets=eurovision_ordered,
            output_folder=dir_path,
            dimension="frame elements",
            figsize=(8,4),
            verbose=2)
