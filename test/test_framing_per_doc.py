import sys
import os
import json
sys.path.append('../../')

from participant_analysis import framing_an_incident_per_doc, dir_path
from datetime import datetime

with open('../DFNDataReleases/structured/inc2lang2doc2subevents.json', "r") as infile:
    subevents_dict = json.load(infile)

song_contest = "Q30973589"
song_contest_date = datetime(2021,5,18)

mh17 = "Q17374096"
mh17_date = datetime(2014,7,17)

utrecht_shooting = "Q62090804"
utrecht_shooting_date = datetime(2019,3,18)

dutch_curfew_riots = "Q105077032"
dutch_curfew_riots_date = datetime(2021,1,23)

framing_an_incident_per_doc(project="test_release",
                            incident=song_contest,
                            language="en",
                            event_date=song_contest_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=song_contest,
                            language="nl",
                            event_date=song_contest_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=mh17,
                            language="nl",
                            event_date=mh17_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=mh17,
                            language="en",
                            event_date=mh17_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=utrecht_shooting,
                            language="nl",
                            event_date=utrecht_shooting_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=utrecht_shooting,
                            language="en",
                            event_date=utrecht_shooting_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=dutch_curfew_riots,
                            language="nl",
                            event_date=dutch_curfew_riots_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)

framing_an_incident_per_doc(project="test_release",
                            incident=dutch_curfew_riots,
                            language="en",
                            event_date=dutch_curfew_riots_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)




#sys.exit()
