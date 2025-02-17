import sys
import os
sys.path.append('../../')

from participant_analysis import compounds, participant_info, dir_path

exclude_fes = ["Cause_harm@Cause", #exclude consistent misclassified FEs
                "Violence@Aggressors",
                "Violence@Cause"]

###compound info###
direct_participants = ["Q1631025548534", #victims
                        "Q1637127625151", #suspect1
                        "Q1637127644242", #suspect2
                        "Q1637127655450", #suspect3
                        "Q1637127680472", #suspect4
                        "Q1632409367599", #victims
                        "Q62116513", #Gökmen Tanis
                        "Q1646212736373", #rioters
                        "Q1646212706669",
                        "Q1638962685452",
                                                "Q1646835057489",
                                                "Q15265344",
                                                "Q56884561",
                                                "Q28109988",
                                                "Q1028",
                                                "Q55614888",
                                                "Q64775156",
                                                "Q19666292",
                                                "Q65295873",
                                                "Q3784982",
                                                "Q700468",
                                                "Q9302874",
                                                "Q11068745",
                                                "Q86747390",
                                                "Q21524985",
                                                "Q61696740",
                                                "Q21621351",
                                                "Q433039",
                                                "Q29",
                                                "Q233",
                                                "Q36",
                                                "Q189",
                                                "Q218",
                                                "Q35",
                                                "Q18002773",
                                                "Q15991875",
                                                "Q1075994",
                                                "Q262386",
                                                "Q2302267",
                                                "Q54718",
                                                "Q366567",
                                                "Q155702",
                                                "Q1305972",
                                                "Q7951164",
                                                "Q1431841",
                                                "Q727176",
                                                "Q649618",
                                                "Q2280893",
                                                "Q722715",
                                                "Q366507",
                                                "Q2611481",
                                                "Q935960",
                                                "Q83389"]

#preprocessing
#wikidata entries for locations
incident_location_ids = {"Q30973589", "Q105077032", "Q62090804", "Q17374096", "Q1309", "Q273746", "Q10002", "Q793", "Q145845", "Q992", "Q9871",
                        "Q26432", "Q9934", "Q34370", "Q36600", "Q9832", "Q727", "Q55", "Q9844", "Q40844", "Q2766547", "Q803",
                        "Q1631864271612"}
#compounds not linked to participants
incident_location_lemmas = {"repatriëringsmissie", "songfestival", "tramaanslag", "doodschieten", "schietpartij", "moordpartij", "updateeen", "geweldpleging", "vliegramp",
                            "rampplek", "schietincident", "goedwillend", "rampgebied", "mh17-ramp", "mh17-proce", "mh17-repatri\u00ebringmissie"
                            "zoeklocatie", "mh17-onderzoek", "afvuurlocatie", "crashsite", "vliegtuigcrash", "luchtruim", "crashplek",
                            "oorlogsgebied"}

compounds(output_folder=dir_path,
            direct_participants=direct_participants,
            identifiers_to_neglect=incident_location_ids,
            compounds_to_exclude=incident_location_lemmas,
            verbose=2)

utrecht = "Q62090804"
selected_participants = {"Q1632409367599": "victims",
                        "Q62116513": "Gökmen Tanis",
                        "Q1689167507986": "police officers",
                        "Q1689168342258": "other suspects",
                        "Q1689169851078": "Utrecht citizens"}
time_buckets_utrecht = {"0-1":range(0,2),
                        "37-703":range(37,704)}

participant_info(incident=utrecht,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_utrecht,
                    output_folder=dir_path,
                    language="nl",
                    verbose=3)

time_buckets_utrecht = {"0":range(0,1),
                        "1":range(1,2),
                        "4-12":range(4,13),
                        "37-703":range(37,704)}

participant_info(incident=utrecht,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_utrecht,
                    output_folder=dir_path,
                    exclude_fes=exclude_fes,
                    unexpressed=True,
                    verbose=3)

song_contest = "Q30973589"

selected_participants = {"Q1638962685452": "participants",
                        "Q1646835057489": "audience",
                        "Q1651075371225": "organizers",
                        "Q166400": "European Broadcasting Union",
                        "Q15265344": "broadcasters",
                        "Q56884561": "Måneskin", #participants
                        "Q28109988": "Jeangu Macrooy",
                        "Q1028": "Jeangu Macrooy",
                        "Q55614888": "James Newman",
                        "Q64775156": "Eden Alene",
                        "Q19666292": "Montaigne",
                        "Q65295873": "Vasil Garvanliev",
                        "Q3784982": "Lesley Roy",
                        "Q700468": "Vincent Bueno",
                        "Q9302874": "Rafał Brzozowski",
                        "Q11068745": "Ben Cristovao",
                        "Q86747390": "Gagnamagnið",
                        "Q21524985": "Destiny Chukunyere",
                        "Q61696740": "Stefania",
                        "Q21621351": "Victoria Georgieva",
                        "Q433039": "Natalia Gordienko",
                        "Q29": "Spain",
                        "Q233": "Malta",
                        "Q36": "Poland",
                        "Q189": "Iceland",
                        "Q218": "Romania",
                        "Q35": "Denmark",
                        "Q18002773": "Avrotros", #broadcasters
                        "Q15991875": "Stichting Nederlandse Publieke Omroep",
                        "Q1075994": "Special Broadcasting Service",
                        "Q262386": "Österreichischer Rundfunk",
                        "Q2302267": "Eesti Rahvusringhääling",
                        "Q54718": "Yle",
                        "Q366567": "Radio Television of Kosovo",
                        "Q155702": "Radio Télévision Luxembourg",
                        "Q1305972": "Ràdio i Televisió d'Andorra",
                        "Q7951164": "WJFD-FM",
                        "Q1431841": "Radio FM",
                        "Q727176": "Radio and Television of Slovakia",
                        "Q649618": "Rádio e Televisão de Portugal",
                        "Q2280893": "Radio Television of BH",
                        "Q722715": "Radio Televizija Crne Gore",
                        "Q366507": "Radio Television of Serbia",
                        "Q2611481": "Sveriges Radio P4",
                        "Q935960": "TV3",
                        "Q83389": "Turkish Radio and Television Corporation"}
time_buckets_contest = {"-730--423": range(-730,-423),
                        "-90-13": range(-90,14)}
to_be_bundled = {"participants": ["participants", "Måneskin", "Jeangu Macrooy", "James Newman", "Eden Alene", "Montaigne",
                                "Vasil Garvanliev", "Lesley Roy", "Vincent Bueno", "Rafał Brzozowski", "Ben Cristovao",
                                "Gagnamagnið", "Destiny Chukunyere", "Stefania", "Victoria Georgieva", "Natalia Gordienko",
                                "Spain", "Malta", "Poland", "Iceland", "Romania","Denmark"],
                "broadcasters": ["broadcasters", "Avrotros", "Stichting Nederlandse Publieke Omroep", "Special Broadcasting Service",
                                "Österreichischer Rundfunk", "Eesti Rahvusringhääling", "Yle", "Radio Television of Kosovo",
                                "Radio Télévision Luxembourg", "Ràdio i Televisió d'Andorra", "WJFD-FM", "Radio FM",
                                "Radio and Television of Slovakia", "Rádio e Televisão de Portugal", "Radio Television of BH",
                                "Radio Televizija Crne Gore", "Radio Television of Serbia", "Sveriges Radio P4", "TV3",
                                "Turkish Radio and Television Corporation"]}

participant_info(incident=song_contest,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_contest,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    language="en",
                    verbose=3)

participant_info(incident=song_contest,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_contest,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    language="nl",
                    verbose=3)

selected_participants = {"Q1631025548534": "victims",
                        "Q159": "Russian government",
                        "Q1673010005817": "relatives",
                        "Q1637127625151": "Oleg Poelatov",
                        "Q1637127644242": "Sergej Doebinski",
                        "Q1637127655450": "Igor Girkin",
                        "Q1637127680472": "Leonid Chartsjenko",
                        "Q1631864085791": "pro-Russian rebels",
                        "Q1632916239145": "bemanningsleden"}

time_buckets_mh17 = {"0-15": range(0,16),
                    "318-1728": range(318,1729)}
to_be_bundled = {"suspects": ["Oleg Poelatov", "Sergej Doebinski", "Igor Girkin", "Leonid Chartsjenko"],
                "victims": ["victims", "bemanningsleden"]}
mh17 = "Q17374096"

participant_info(incident=mh17,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_mh17,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    language="en",
                    verbose=3)

participant_info(incident=mh17,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_mh17,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    language="nl",
                    verbose=3)

curfew = "Q105077032"
selected_participants = {"Q1646212736373": "rioters",
                        "Q1646212706669": "law enforcement",
                        "Q4310949": "Dutch government",
                        "Q1646237450270": "entrepeneurs",
                        "Q1720602541245": "citizens"}
time_buckets_curfew = {"0-2": range(0,3),
                    "4-7": range(4,8)}

participant_info(incident=curfew,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_curfew,
                    output_folder=dir_path,
                    language="en",
                    verbose=3)

participant_info(incident=curfew,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_curfew,
                    output_folder=dir_path,
                    language="nl",
                    verbose=3)
#sys.exit()

song_contest = "Q30973589"

selected_participants = {"Q1638962685452": "participants",
                        "Q1646835057489": "audience",
                        "Q1651075371225": "organizers",
                        "Q166400": "European Broadcasting Union",
                        "Q15265344": "broadcasters",
                        "Q56884561": "Måneskin", #participants
                        "Q28109988": "Jeangu Macrooy",
                        "Q1028": "Jeangu Macrooy",
                        "Q55614888": "James Newman",
                        "Q64775156": "Eden Alene",
                        "Q19666292": "Montaigne",
                        "Q65295873": "Vasil Garvanliev",
                        "Q3784982": "Lesley Roy",
                        "Q700468": "Vincent Bueno",
                        "Q9302874": "Rafał Brzozowski",
                        "Q11068745": "Ben Cristovao",
                        "Q86747390": "Gagnamagnið",
                        "Q21524985": "Destiny Chukunyere",
                        "Q61696740": "Stefania",
                        "Q21621351": "Victoria Georgieva",
                        "Q433039": "Natalia Gordienko",
                        "Q29": "Spain",
                        "Q233": "Malta",
                        "Q36": "Poland",
                        "Q189": "Iceland",
                        "Q218": "Romania",
                        "Q35": "Denmark",
                        "Q18002773": "Avrotros", #broadcasters
                        "Q15991875": "Stichting Nederlandse Publieke Omroep",
                        "Q1075994": "Special Broadcasting Service",
                        "Q262386": "Österreichischer Rundfunk",
                        "Q2302267": "Eesti Rahvusringhääling",
                        "Q54718": "Yle",
                        "Q366567": "Radio Television of Kosovo",
                        "Q155702": "Radio Télévision Luxembourg",
                        "Q1305972": "Ràdio i Televisió d'Andorra",
                        "Q7951164": "WJFD-FM",
                        "Q1431841": "Radio FM",
                        "Q727176": "Radio and Television of Slovakia",
                        "Q649618": "Rádio e Televisão de Portugal",
                        "Q2280893": "Radio Television of BH",
                        "Q722715": "Radio Televizija Crne Gore",
                        "Q366507": "Radio Television of Serbia",
                        "Q2611481": "Sveriges Radio P4",
                        "Q935960": "TV3",
                        "Q83389": "Turkish Radio and Television Corporation"}

time_buckets_contest = {"-730--620": range(-730,-619),
                        "-604--470": range(-604,-469),
                        "-465--424": range(-465,-423),
                        "-419--242": range(-419,-241),
                        "-90--28": range(-90,-27),
                        "-26--1": range(-26,0),
                        "0-13": range(0,14)}

to_be_bundled = {"participants": ["participants", "Måneskin", "Jeangu Macrooy", "James Newman", "Eden Alene", "Montaigne",
                                "Vasil Garvanliev", "Lesley Roy", "Vincent Bueno", "Rafał Brzozowski", "Ben Cristovao",
                                "Gagnamagnið", "Destiny Chukunyere", "Stefania", "Victoria Georgieva", "Natalia Gordienko",
                                "Spain", "Malta", "Poland", "Iceland", "Romania","Denmark"],
                "broadcasters": ["broadcasters", "Avrotros", "Stichting Nederlandse Publieke Omroep", "Special Broadcasting Service",
                                "Österreichischer Rundfunk", "Eesti Rahvusringhääling", "Yle", "Radio Television of Kosovo",
                                "Radio Télévision Luxembourg", "Ràdio i Televisió d'Andorra", "WJFD-FM", "Radio FM",
                                "Radio and Television of Slovakia", "Rádio e Televisão de Portugal", "Radio Television of BH",
                                "Radio Televizija Crne Gore", "Radio Television of Serbia", "Sveriges Radio P4", "TV3",
                                "Turkish Radio and Television Corporation"]}

participant_info(incident=song_contest,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_contest,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    unexpressed=True,
                    verbose=3)
#sys.exit()
selected_participants = {"Q1631025548534": "victims",
                        "Q159": "Russian government",
                        "Q1673010005817": "relatives",
                        "Q1637127625151": "Oleg Poelatov",
                        "Q1637127644242": "Sergej Doebinski",
                        "Q1637127655450": "Igor Girkin",
                        "Q1637127680472": "Leonid Chartsjenko",
                        "Q1631864085791": "pro-Russian rebels",
                        "Q1632916239145": "bemanningsleden"}

time_buckets_mh17 = {"0-1": range(0,2),
                    "2-7": range(2,8),
                    "8-15": range(8,16),
                    "19-130": range(19,131),
                    "318-806": range(318,807),
                    "1084-1728": range(1084,1729)}

to_be_bundled = {"suspects": ["Oleg Poelatov", "Sergej Doebinski", "Igor Girkin", "Leonid Chartsjenko"],
                "victims": ["victims", "bemanningsleden"]}

mh17 = "Q17374096"

participant_info(incident=mh17,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_mh17,
                    output_folder=dir_path,
                    to_be_bundled=to_be_bundled,
                    unexpressed=True,
                    verbose=3)

curfew = "Q105077032"
selected_participants = {"Q1646212736373": "rioters",
                        "Q1646212706669": "law enforcement",
                        "Q4310949": "Dutch government",
                        "Q1646237450270": "entrepeneurs",
                        "Q1720602541245": "citizens"}
time_buckets_curfew = {"0-2": range(0,3),
                    "3": range(3,4),
                    "4-7": range(4,8)}

participant_info(incident=curfew,
                    selected_participants=selected_participants,
                    time_buckets=time_buckets_curfew,
                    output_folder=dir_path,
                    exclude_fes=exclude_fes,
                    unexpressed=True,
                    verbose=3)
