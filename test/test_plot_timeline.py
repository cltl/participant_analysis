import sys
import os
import json
sys.path.append('../../')

from participant_analysis import plot_timeline, dir_path

utrecht_shooting = "Q62090804"
eurovision = "Q30973589"
mh17 = "Q17374096"
mh17_titles_to_ignore = ["Legerhelikopter Oekraïne neergehaald", "Video 'shows military plane downed'"]
dutch_curfew_riots = "Q105077032"
riots_titles_to_ignore = ["Regionale avondklok? Niet je hond uitlaten, en alleen met toestemming straat op"]

plot_timeline(incident=utrecht_shooting,
                output_folder=dir_path,
                start_from_scratch=False,
                verbose=1)

plot_timeline(incident=mh17,
                output_folder=dir_path,
                titles_to_ignore=mh17_titles_to_ignore,
                start_from_scratch=False,
                verbose=1)

plot_timeline(incident=dutch_curfew_riots,
                output_folder=dir_path,
                titles_to_ignore=riots_titles_to_ignore,
                start_from_scratch=False,
                verbose=1)

plot_timeline(incident=eurovision,
                output_folder=dir_path,
                start_from_scratch=False,
                verbose=1)

#sys.exit()
