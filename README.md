### Framing Participant Analysis
This package provides functions that extract linguistic information from a corpus of reference texts grouped under the same incident and perform a frame semantic analysis of the referenced participants over time. Specifically, the package provides distribution over time of in-text mentions that are linked to structured data, and it provides a distribution of the frames with which the same mentions are annotated.

This package was built and used for the purpose of a thesis Chapter titled "Variation in Framing at Participant Level".

### Prerequisites
Python 3.7.4 was used to create this package. It might work with older versions of Python.

### Resources
A number of GitHub repositories need to be cloned and adapted with novel data. This can be done calling:
```bash
bash install.sh
```

### Python modules
A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

### Usage
This package comes with different main functions:

# Extract frame semantic information from FramInc corpus
The function framing_an_incident_per_doc() extracts linguistic information from the annotated NAF files (the FramInc corpus) in the DFNDataReleases repository. You can run the function with the following command:

```python
from incident_analysis import framing_an_incident_per_doc, dir_path
from datetime import datetime
import json

with open('../DFNDataReleases/structured/inc2lang2doc2subevents.json', "r") as infile:
    subevents_dict = json.load(infile)

utrecht_shooting = "Q62090804"
utrecht_shooting_date = datetime(2019,3,18)

framing_an_incident_per_doc(project="test_release",
                            incident=utrecht_shooting,
                            language="nl",
                            event_date=utrecht_shooting_date,
                            subevents_dict=subevents_dict,
                            output_folder=dir_path,
                            start_from_scratch=False,
                            verbose=1)
```
The following parameters are specified:
* **project** the label of the research project
* **incident** the wikidata identifier of the incident
* **language** the language in which the reference texts are overwritten
* **event_date** the date on which the incident occurred.
* **subevents_dict** a dictionary that links a selection of mentions in FramInc to the incident ID, as a means of post-annotation curation.
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which extracted data will be exported.
* **start_from_scratch**: if True, remove all existing output
* **verbose**: 1: descriptive stats 2: more stats 3: lots of stats

After running the example, you observe an **output** folder in this directory. Its nested structure is as follows:

output
  WIKIDATA_ID
    corpus
      LANGUAGE
        *.json

Run the python script test_framing_per_doc.py in the **test** folder to extract and export the information from all four incidents in FramInc in English and Dutch to the output folder.

# Plot timeline
The function plot_timeline() takes the json files from a specified incident and exports a plot of publication dates. You can run the function with the following command:

```python
from participant_analysis import plot_timeline, dir_path

utrecht_shooting = "Q62090804"

plot_timeline(incident=utrecht_shooting,
                output_folder=dir_path,
                start_from_scratch=False,
                verbose=1)
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which extracted data will be exported.
* **start_from_scratch**: if True, remove all existing output
* **verbose**: 1: print path to which the plot is exported.

After running the example, you will find a timeline.PDF in the WIKIDATA_ID subfolder of **output**.

Run the python script test_plot_timeline.py in the **test** folder to plot the timelines of all four incidents in FramInc.

# participant information to json
The function participant_info() extracts information from the previously created jsons and groups that information per specified participant and per temporal distance class. You can run the function with the following command:

```python
from participant_analysis import participant_analysis, dir_path

utrecht_shooting = "Q62090804"
selected_participants = {"Q1632409367599": "victims",
                        "Q62116513": "Gökmen Tanis",
                        "Q1689167507986": "police officers",
                        "Q1689168342258": "other suspects",
                        "Q1689169851078": "Utrecht citizens"}
time_buckets = {"0":range(0,1),
                "1":range(1,2),
                "4-12":range(4,13),
                "37-703":range(37,704)}

incident_info(incident=utrecht_shooting,
                  time_buckets=time_buckets_utrecht,
                  output_folder=dir_path,
                  verbose=3)
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **time_buckets** dictionary of temporal distance classes
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the new json file will be exported.
* **verbose**: >=1: print statistics and export paths; >=2: print more statistics

After running the example, you will find the new json folder in the WIKIDATA_ID subfolder of **output**. Run the python script test_participant_info.py in the **test** folder to produce the json folders of all four incidents in FramInc.

# Reference Analysis
The function references() runs an analysis of the entity-linked mentions and plots their relative distribution across temporal distance classes. You can run the function with the following command:

```python
from participant_analysis import references, dir_path
import json

utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"

with open(f"{dir_path}/output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_d = json.load(infile)

    references(incident=utrecht_shooting,
                participants_d=utrecht_participants_d,
                ordered_l=utrecht_ordered,
                output_folder=dir_path,
                dimension="lemmas",
                verbose=1)
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **participants_dict** dictionary of frame semantic information grouped under temporal distance classes and participants
* **ordered_l** a list with the temporal distance classes in fixed order
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the plots will be exported
* **dimension** the object of analysis
* **verbose**: >=1: print path to pdf or tex file

After running the example, you observe a **figures** folder in the respective WIKIDATA_ID subfolder of **output**. Its nested structure is as follows:

output
  WIKIDATA_TD
    figures
      references
        *.pdf

Run the python script test_references.py in the **test** folder to produce reference plots for all four incidents in FramInc.

# Frame element analysis
The function fe_analysis() runs an analysis of the frame elements and plots their relative distribution across temporal distance classes. You can run the function with the following command:

```python
from participant_analysis import fe_analysis, dir_path
import json

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

```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **data_dict** dictionary of frame semantic information grouped under temporal distance classes and participants
* **ordered_time_buckets** a list with the temporal distance classes in fixed order
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the plots will be exported
* **verbose**: >=1: print path to pdf or tex file; >=2: print descriptive stats

After running the example, plots are exported to the **frame elements** subfolder of **figures**. Run the python script test_frame_element_analysis.py in the **test** folder to produce frame element plots for all four incidents in FramInc.

#Lexical unit analysis
The function lu_analysis() runs an analysis of the lexical units and plots their pos distribution (noun versus proper noun) across temporal distance classes per participant. You can run the function with the following command:

```python
import json
from participant_analysis import lu_analysis, dir_path

#Utrecht
utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_participants_d = json.load(infile)

lu_analysis(incident=utrecht_shooting,
            participant_d=utrecht_participants_d,
            ordered_l=utrecht_ordered,
            output_folder=dir_path,
            n_time_buckets=len(utrecht_ordered),
            verbose=1)
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **participant_dict** dictionary of frame semantic information grouped under temporal distance classes
* **ordered_l** a list with the temporal distance classes in fixed order
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the plots will be exported
* **n_time_buckets** the number of time buckets determined for this incident
* **verbose**: >=1: print path to pdf file; >=2: print descriptive statistics

After running the example, barplots are exported to the **lexical units** subfolder of **figures**. Run the python script test_lexical_unit_analysis.py in the **test** folder to produce lexical unit barplots for all four incidents in FramInc. It also exports tables with descriptive statistics on compounds and overall type-token distributions.

#Construction analysis
The function construction_analysis() runs an analysis of constructions and plots their relative distribution across temporal distance classes. You can run the function with the following command:

```python
from participant_analysis import construction_analysis, dir_path
import json

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
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **data_d** dictionary of frame semantic information grouped under temporal distance classes
* **ordered_l** a list with the temporal distance classes in fixed order
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the plots will be exported
* **colors** list of colors that are used in plotting
* **verbose**: >=1: print path to pdf file

After running the example, plots are exported to the **constructions** subfolder of **figures**. Run the python script test_construction_analysis.py in the **test** folder to produce construction plots for all four incidents in FramInc.

#Interface analysis
The function interface_analysis() runs an analysis of the frame elements' interfaces and plots their relative distribution across temporal distance classes. You can run the function with the following command:

```python
from participant_analysis import interface_analysis, dir_path
import json

utrecht_ordered = ["0","1","4-12","37-703"]
utrecht_shooting = "Q62090804"
with open(f"../output/{utrecht_shooting}/participants_info.json", "r") as infile:
    utrecht_participants_d = json.load(infile)

with open(f"../output/{utrecht_shooting}/unexpressed_fes_info.json", "r") as infile:
    utrecht_unexpressed_d = json.load(infile)

interface_analysis(incident=utrecht_shooting,
            participants_d=utrecht_participants_d,
            unexpressed_d=utrecht_unexpressed_d,
            ordered_l=utrecht_ordered,
            output_folder=dir_path,
            verbose=1)
```
The following parameters are specified:
* **incident** the wikidata identifier of the incident
* **participants_d** dictionary of frame semantic information grouped under temporal distance classes
* **unexpressed_d** dictionary of the unexpressed frame elements grouped under temporal distance classes
* **ordered_l** a list with the temporal distance classes in fixed order
* **output_folder** the path to the current package. The helper functions will use this path to create new folders to which the plots will be exported
* **verbose**: >=1: print path to pdf file, >=2: print descriptive stats

After running the example, plots are exported to the **interfaces** subfolder of **figures** and tables are exported to the **tables** subfolder. Run the python script test_interface_analysis.py in the **test** folder to produce interface plots and tables for all four incidents in FramInc.

### Authors
* **Levi Remijnse** (levi_remijnse@hotmail.com)

### License
This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
