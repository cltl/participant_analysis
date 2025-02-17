import sys
import os
import json
sys.path.append('../../')

from participant_analysis import lu_analysis, compounds, dir_path

with open(f"../output/compounds.json", "r") as infile:
    compounds_d = json.load(infile)

lu_analysis(incident=None,
            participant_d=compounds_d,
            ordered_l=None,
            output_folder=dir_path,
            compounds=True,
            verbose=1)

#Utrecht
utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_participants_d = json.load(infile)

lu_analysis(incident=utrecht_shooting,
            participant_d=utrecht_participants_d,
            ordered_l=utrecht_ordered,
            output_folder=dir_path,
            n_time_buckets=4,
            verbose=1)

with open(f"../output/{utrecht_shooting}/participants_info_nl.json", "r") as infile:
    utrecht_participants_nl_d = json.load(infile)

lu_analysis(incident=utrecht_shooting,
            participant_d=utrecht_participants_nl_d,
            ordered_l=utrecht_ordered,
            output_folder=dir_path,
            language="nl",
            verbose=1)

#mh17
mh17_ordered = ["0-1","2-7","8-15","19-130","318-806",
                "1084-1728"]
mh17 = "Q17374096"
with open(f"../output/{mh17}/participants_info.json", "r") as infile:
    mh17_participants_d = json.load(infile)

lu_analysis(incident=mh17,
            participant_d=mh17_participants_d,
            ordered_l=mh17_ordered,
            output_folder=dir_path,
            n_time_buckets=6,
            verbose=1)

with open(f"../output/{mh17}/participants_info_en.json", "r") as infile:
    mh17_participants_en_d = json.load(infile)

lu_analysis(incident=mh17,
            participant_d=mh17_participants_en_d,
            ordered_l=mh17_ordered,
            output_folder=dir_path,
            language="en",
            verbose=1)

#curfew riots
curfew_ordered = ["0-2", "3", "4-7"]
dutch_curfew_riots = "Q105077032"
with open(f"../output/{dutch_curfew_riots}/participants_info.json", "r") as infile:
    curfew_participants_d = json.load(infile)

lu_analysis(incident=dutch_curfew_riots,
            participant_d=curfew_participants_d,
            ordered_l=curfew_ordered,
            output_folder=dir_path,
            n_time_buckets=3,
            verbose=1)

with open(f"../output/{dutch_curfew_riots}/participants_info_nl.json", "r") as infile:
    curfew_participants_nl_d = json.load(infile)

lu_analysis(incident=dutch_curfew_riots,
            participant_d=curfew_participants_nl_d,
            ordered_l=curfew_ordered,
            output_folder=dir_path,
            language="nl",
            verbose=1)

#eurovision
eurovision_song_contest = "Q30973589"
eurovision_ordered = ["-730--620","-604--470","-465--424",
                      "-419--242","-90--28","-26--1","0-13"]
with open(f"../output/{eurovision_song_contest}/participants_info.json", "r") as infile:
    eurovision_participants_d = json.load(infile)

lu_analysis(incident=eurovision_song_contest,
            participant_d=eurovision_participants_d,
            ordered_l=eurovision_ordered,
            output_folder=dir_path,
            n_time_buckets=7,
            verbose=1)

with open(f"../output/{eurovision_song_contest}/participants_info_en.json", "r") as infile:
    eurovision_participants_en_d = json.load(infile)

lu_analysis(incident=eurovision_song_contest,
            participant_d=eurovision_participants_en_d,
            ordered_l=eurovision_ordered,
            output_folder=dir_path,
            language="en",
            verbose=1)
