import sys
import os
import json
sys.path.append('../../')

from participant_analysis import derive_entropy, dir_path

#Utrecht
utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_d = json.load(infile)

with open(f"../output/{utrecht_shooting}/unexpressed_fes_info.json", "r") as infile:
    utrecht_unexpressed_d = json.load(infile)

#mh17
mh17_ordered = ["0-1","2-7","8-15","19-130","318-806",
                "1084-1728"]
mh17 = "Q17374096"
with open(f"../output/{mh17}/participants_info.json", "r") as infile:
    mh17_d = json.load(infile)

with open(f"../output/{mh17}/unexpressed_fes_info.json", "r") as infile:
    mh17_unexpressed_d = json.load(infile)

#curfew riots
curfew_ordered = ["0-2", "3", "4-7"]
dutch_curfew_riots = "Q105077032"
with open(f"../output/{dutch_curfew_riots}/participants_info.json", "r") as infile:
    curfew_d = json.load(infile)

with open(f"../output/{dutch_curfew_riots}/unexpressed_fes_info.json", "r") as infile:
    curfew_unexpressed_d = json.load(infile)

#eurovision
eurovision_song_contest = "Q30973589"
eurovision_ordered = ["-730--620","-604--470","-465--424",
                      "-419--242","-90--28","-26--1","0-13"]
with open(f"../output/{eurovision_song_contest}/participants_info.json", "r") as infile:
    eurovision_d = json.load(infile)

with open(f"../output/{eurovision_song_contest}/unexpressed_fes_info.json", "r") as infile:
    eurovision_unexpressed_d = json.load(infile)

derive_entropy(utrecht_d=utrecht_d,
                    utrecht_ordered=utrecht_ordered,
                    mh17_d=mh17_d,
                    mh17_ordered=mh17_ordered,
                    curfew_d=curfew_d,
                    curfew_ordered=curfew_ordered,
                    eurovision_d=eurovision_d,
                    eurovision_ordered=eurovision_ordered,
                    feature="frame elements",
                    output_folder=dir_path,
                    unexpressed_dicts=[utrecht_unexpressed_d,
                                        mh17_unexpressed_d,
                                        curfew_unexpressed_d,
                                        eurovision_unexpressed_d],
                    verbose=1)

derive_entropy(utrecht_d=utrecht_d,
                    utrecht_ordered=utrecht_ordered,
                    mh17_d=mh17_d,
                    mh17_ordered=mh17_ordered,
                    curfew_d=curfew_d,
                    curfew_ordered=curfew_ordered,
                    eurovision_d=eurovision_d,
                    eurovision_ordered=eurovision_ordered,
                    feature="sentence realizations",
                    output_folder=dir_path,
                    verbose=1)

derive_entropy(utrecht_d=utrecht_d,
                    utrecht_ordered=utrecht_ordered,
                    mh17_d=mh17_d,
                    mh17_ordered=mh17_ordered,
                    curfew_d=curfew_d,
                    curfew_ordered=curfew_ordered,
                    eurovision_d=eurovision_d,
                    eurovision_ordered=eurovision_ordered,
                    feature="discourse realizations",
                    output_folder=dir_path,
                    verbose=1)

#sys.exit()
