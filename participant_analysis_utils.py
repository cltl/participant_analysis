from collections import defaultdict, Counter
import glob
import json
import collections
import pickle

def get_frequency_ranking_of_participants(output_folder, incident, verbose=0):
    """get a frequency ranking of structured data"""
    participant_mentions = defaultdict(list)
    dev = []

    for folder in glob.glob(f"{output_folder}/output/{incident}/corpus/*"):
        for filename in glob.glob(f"{folder}/*"):
            with open(filename, 'r') as infile:
                json_dict = json.load(infile)
                title = "".join([key for key, value in json_dict.items()])
                historical_distance = json_dict[title]["historical distance"]
                dev.append((title, historical_distance))
                for identifier, targets in json_dict[title]["frames/links"].items():
                    if identifier != incident:
                        for target in targets.keys():
                            participant_mentions[identifier].append(target)

    if verbose:
        print("frequency ranking of mentions:")
        with open(f"../DFNDataReleases/structured/inc2str_index.json", 'r') as infile:
                labels_dict = json.load(infile)
        for participant, mentions in participant_mentions.items():
            for label in labels_dict[incident]["sem:hasActor"]:
                if participant in label:
                    final_label = label.split('| ')[1]
                else:
                    for label in labels_dict[incident]["sem:hasPlace"]:
                        if participant in label:
                            final_label = label.split('| ')[1]
            print(len(mentions), participant, final_label)

    sorted_dev = sorted([tupl[1] for tupl in dev])
    return participant_mentions, sorted_dev

def compile_terms(info_d):
    terms_d = {}
    for wiki_id, info in info_d["frames/links"].items():
        for term, d in info.items():
            terms_d[term] = d
    for term, d in info_d["subevents"].items():
        terms_d[term] = d
    for term, d in info_d["fe's without links"].items():
        terms_d[term] = d
    return terms_d

def check_interface_status(info_d, terms_d, fe_pred, fe_sentence):
    if info_d["frame"] != None:
        frame_pred = info_d["frame"][1]
        if frame_pred == fe_pred:
            return "word"

    for term, info in terms_d.items():
        if "frame" in info.keys():
            if info["frame"] != None:
                if "sentence" in info.keys():
                    frame_pred = info["frame"][1]
                    sentence = info["sentence"]
                    if frame_pred == fe_pred and sentence == fe_sentence: #if the fe belongs to the frame and both are in the same sentence
                        return "sentence"
                    elif frame_pred == fe_pred and sentence != fe_sentence: #if the fe belongs to the frame but both are in different sentences
                        return "discourse"
                    else:
                        continue

def misclassified_incident(json_dict, incident, target, verbose):
    """check if the target is also linked to the incident"""
    if incident in json_dict.keys():
        for term, info in json_dict[incident].items():
            if term == target:
                return True
    return False

def correct_spelling(compound):
    if compound.startswith("hoofdverdach"):
        new_lemma = "hoofdverdachte"
    elif compound.startswith("mh17-verdach"):
        new_lemma = "mh17-verdachte"
    elif compound.startswith("zwaargewond"):
        new_lemma = "zwaargewonde"
    else:
        new_lemma = compound
    return new_lemma

def info_participant(identifier, time_buckets, incident, output_folder, language, verbose=0):
    """extract information about participant per time bucket"""
    fes_to_remove = {"Rebellion@Current_order", "Rebellion@Current_leadership"}
    participant_info = {}

    for time_bucket in time_buckets.keys():
        participant_info[time_bucket] = defaultdict(list)
    if language == None:
        for folder in glob.glob(f"{output_folder}/output/{incident}/corpus/*"):
            for filename in glob.glob(f"{folder}/*"):
                with open(filename, 'r') as infile:
                    json_dict = json.load(infile)
                title = "".join([key for key, value in json_dict.items()]) #get title
            #    print(title)
                terms_d = compile_terms(json_dict[title])
                if identifier not in json_dict[title]["frames/links"].keys(): #check if entity is in doc
                    continue
                else:
                    historical_distance = json_dict[title]["historical distance"] #get historical distance
                    for bucket, rang in time_buckets.items():
                        if historical_distance in rang: #in which time bucket does this doc belong?
                            participant_info[bucket]["titles"].append(title)
                            for target, info in json_dict[title]["frames/links"][identifier].items():
                                if misclassified_incident(json_dict[title]["frames/links"], incident, target, verbose) == True: #check if the target is linked to the incident
                                    continue
                                else:
                                    if "sentence" in info.keys():
                                        fe_sentence = info["sentence"]
                                        if info["frame elements"] != None:
                                            for tupl in info["frame elements"]:
                                                fe = tupl[0]
                                                fe_pred = tupl[1]
                                                if fe in fes_to_remove:
                                                    continue
                                                else:
                                                    participant_info[bucket]["frame elements"].append(fe) #append fe
                                                    if check_interface_status(info, terms_d, fe_pred, fe_sentence) == "word":
                                                        participant_info[bucket]["lexical realizations"].append(fe)
                                                    elif check_interface_status(info, terms_d, fe_pred, fe_sentence) == "sentence":
                                                        participant_info[bucket]["sentence realizations"].append(fe)
                                                    else:
                                                        participant_info[bucket]["discourse realizations"].append(fe)
                                        if "compound" in info.keys():
                                            if info["function"] == "head":
                                                compound = info["compound"].lower()
                                                lemma = correct_spelling(compound)
                                                participant_info[bucket]["lemmas"].append(lemma) #append lemma
                                                participant_info[bucket]["compounds"].append(lemma)
                                                pos = info["POS"]
                                                dep = info["syntactic relation"]
                                                participant_info[bucket]["POS"].append(pos) #append pos
                                                participant_info[bucket]["syntactic function"].append(dep)
                                                if pos == "NOUN" and info["frame"] != None:
                                                    participant_info[bucket]["reftype:evokes"].append(lemma)
                                            else:
                                                continue
                                        else:
                                            lemma = info["lemma"]
                                            participant_info[bucket]["lemmas"].append(lemma) #append lemma
                                            pos = info["POS"]
                                            dep = info["syntactic relation"]
                                            participant_info[bucket]["POS"].append(pos) #append pos
                                            participant_info[bucket]["syntactic function"].append(dep)
                                            if pos == "NOUN" and info["frame"] != None:
                                                participant_info[bucket]["reftype:evokes"].append(lemma)
    else:
        for filename in glob.glob(f"{output_folder}/output/{incident}/corpus/{language}/*"):
            with open(filename, 'r') as infile:
                json_dict = json.load(infile)
            title = "".join([key for key, value in json_dict.items()]) #get title
        #    print(title)
            terms_d = compile_terms(json_dict[title])
            if identifier not in json_dict[title]["frames/links"].keys(): #check if entity is in doc
                continue
            else:
                historical_distance = json_dict[title]["historical distance"] #get historical distance
                for bucket, rang in time_buckets.items():
                    if historical_distance in rang: #in which time bucket does this doc belong?
                        participant_info[bucket]["titles"].append(title)
                        for target, info in json_dict[title]["frames/links"][identifier].items():
                            if misclassified_incident(json_dict[title]["frames/links"], incident, target, verbose) == True: #check if the target is linked to the incident
                                continue
                            else:
                                if "sentence" in info.keys():
                                    fe_sentence = info["sentence"]
                                    if info["frame elements"] != None:
                                        for tupl in info["frame elements"]:
                                            fe = tupl[0]
                                            fe_pred = tupl[1]
                                            if fe in fes_to_remove:
                                                continue
                                            else:
                                                participant_info[bucket]["frame elements"].append(fe) #append fe
                                                if check_interface_status(info, terms_d, fe_pred, fe_sentence) == "word":
                                                    participant_info[bucket]["lexical realizations"].append(fe)
                                                elif check_interface_status(info, terms_d, fe_pred, fe_sentence) == "sentence":
                                                    participant_info[bucket]["sentence realizations"].append(fe)
                                                else:
                                                    participant_info[bucket]["discourse realizations"].append(fe)
                                    if "compound" in info.keys():
                                        if info["function"] == "head":
                                            compound = info["compound"].lower()
                                            lemma = correct_spelling(compound)
                                            participant_info[bucket]["lemmas"].append(lemma) #append lemma
                                            participant_info[bucket]["compounds"].append(lemma)
                                            pos = info["POS"]
                                            dep = info["syntactic relation"]
                                            participant_info[bucket]["POS"].append(pos) #append pos
                                            participant_info[bucket]["syntactic function"].append(dep)
                                            if pos == "NOUN" and info["frame"] != None:
                                                participant_info[bucket]["reftype:evokes"].append(lemma)
                                        else:
                                            continue
                                    else:
                                        lemma = info["lemma"]
                                        participant_info[bucket]["lemmas"].append(lemma) #append lemma
                                        pos = info["POS"]
                                        dep = info["syntactic relation"]
                                        participant_info[bucket]["POS"].append(pos) #append pos
                                        participant_info[bucket]["syntactic function"].append(dep)
                                        if pos == "NOUN" and info["frame"] != None:
                                            participant_info[bucket]["reftype:evokes"].append(lemma)
    return participant_info

def extract_info(participants_info):
    "extract and print descriptive statistics"
    for participant, info in participants_info.items():
        mentions = []
        frame_elements = []
        word_level = []
        discourse_level = []
        for tc, info2 in info.items():
            for lemma in info2["lemmas"]:
                mentions.append(lemma)
            for fe in info2["frame elements"]:
                frame_elements.append(fe)
            for w_fe in info2["lexical realizations"]:
                word_level.append(w_fe)
            for d_fe in info2["discourse realizations"]:
                discourse_level.append(d_fe)
        print(participant)
        print("mentions:", len(mentions))
        print("FEs:", len(frame_elements))
        counter = Counter(frame_elements)
        most_common = counter.most_common(3)
        for tupl in most_common:
            fe = tupl[0]
            freq = tupl[1]
            perc = round((freq*100)/len(frame_elements), 1)
            print(fe, freq, f"({perc}%)")
        print("word level FEs:", len(word_level))
        print("discourse level FEs:", len(discourse_level))
        print()
    return

def bundle_participants(participants_info, to_be_bundled, time_buckets):
    """merge information about preselected participants under a new group label"""
    for group_label, l in to_be_bundled.items(): #iterate over to_be_bundled
        new_dict = defaultdict(dict)
        for time_bucket in time_buckets.keys():
            new_dict[time_bucket] = defaultdict(list)
        for identifier, time_buckets in participants_info.copy().items(): #iterate over participants_info Igor
            if identifier in l: #igor in l
                for time_bucket, info in time_buckets.items(): #iterate over time buckets
                    lemmas = info["lemmas"]
                    for lemma in lemmas: #iterate over lemmas
                        new_dict[time_bucket]["lemmas"].append(lemma) #lemma to the right time bucket in new_dict
                    fes = info["frame elements"]
                    for fe in fes:
                        new_dict[time_bucket]["frame elements"].append(fe)
                    lex_rel = info["lexical realizations"]
                    for lex in lex_rel:
                        new_dict[time_bucket]["lexical realizations"].append(lex)
                    discourse_rel = info["discourse realizations"]
                    for t in discourse_rel:
                        new_dict[time_bucket]["discourse realizations"].append(t)
                    pos = info["POS"]
                    for t in pos:
                        new_dict[time_bucket]["POS"].append(t)
                    reftype = info["reftype:evokes"]
                    for ref in reftype:
                        new_dict[time_bucket]["reftype:evokes"].append(ref)
                    syntax = info["syntactic function"]
                    for func in syntax:
                        new_dict[time_bucket]["syntactic function"].append(func)
                    titles = info["titles"]
                    for title in titles:
                        new_dict[time_bucket]["title"].append(title)
                    sentence_rel = info["sentence realizations"]
                    for t in sentence_rel:
                        new_dict[time_bucket]["sentence realizations"].append(t)
                    if "compounds" in info.keys():
                        for c in info["compounds"]:
                            new_dict[time_bucket]["compounds"].append(c)
                del participants_info[identifier]
        participants_info[group_label] = new_dict
    return

def export_unexpressed_fes(anchor_unexpressed_fes_l, climax_unexpressed_fes_l, over_time_d, output_folder, incident, verbose):
    """export unexpressed fes to pickle and json"""
    anchor_pkl_path = f"{output_folder}/output/{incident}/anchor_unexpressed_fes.pkl"
    climax_pkl_path = f"{output_folder}/output/{incident}/climax_unexpressed_fes.pkl"
    over_time_json_path = f"{output_folder}/output/{incident}/unexpressed_fes_info.json"

    with open(anchor_pkl_path, "wb") as f:
        pickle.dump(anchor_unexpressed_fes_l, f)
    with open(climax_pkl_path, "wb") as f:
        pickle.dump(climax_unexpressed_fes_l, f)
    with open(over_time_json_path, 'w') as outfile:
        json.dump(over_time_d, outfile, indent=4, sort_keys=True)

    if verbose:
        print(f"exported unexpressed anchor frame element list to {anchor_pkl_path}")
        print(f"exported unexpressed climax frame element list to {climax_pkl_path}")
        print(f"exported unexpressed frame elements over time info to {over_time_json_path}")
    return

def get_unexpressed_fes(time_buckets, output_folder, incident, exclude_fes):
    """get the unexpressed fes from a corpus.
    If identifier is underspecified, then it extracts all"""
    anchor_unexpressed_fes = []
    over_time_d = {}
    climax_unexpressed_fes = []
    #pprint.pprint(over_time_d)
    for time_bucket in time_buckets.keys():
        over_time_d[time_bucket] = defaultdict(list)

    for folder in glob.glob(f"{output_folder}/output/{incident}/corpus/*"):
        for filename in glob.glob(f"{folder}/*"):
            with open(filename, 'r') as infile:
                json_dict = json.load(infile)

            for title, keys in json_dict.items():
                print(title)
                historical_distance = keys["historical distance"]
                for bucket, rang in time_buckets.items():
                    if historical_distance in rang:
                        anchor_pred_ids = set()
                        if incident in keys["frames/links"]:
                            for term, info in keys["frames/links"][incident].items():
                                if info["frame"] != None:
                                    frame_id = info["frame"][1] #anchor predicate ID
                                    anchor_pred_ids.add(frame_id)
                        for tupl in keys["implicated fe's"]:
                            fe = tupl[0] #implicit FE
                            pred_id = tupl[1] #predicate ID
                            if pred_id in anchor_pred_ids and fe not in exclude_fes:
                                anchor_unexpressed_fes.append(fe)
                                over_time_d[bucket]["anchor"].append(fe)
                            if pred_id not in anchor_pred_ids and fe not in exclude_fes:
                                climax_unexpressed_fes.append(fe)
                                over_time_d[bucket]["non-anchor"].append(fe)
                                print(fe)


    return anchor_unexpressed_fes, climax_unexpressed_fes, over_time_d

def extract_compounds(dpas, output_folder, identifiers_to_neglect, compounds_to_neglect, verbose):
    """extract all compounds from dutch corpus"""
    compound_d = {}
    dpa = []
    ipa = []

    for folder in glob.glob(f"{output_folder}/output/*"):
        for filename in glob.glob(f"{folder}/corpus/nl/*"):
            with open(filename, 'r') as infile:
                json_dict = json.load(infile)

            for title, keys in json_dict.items():
                for participant, terms in keys["frames/links"].items():
                    if participant not in identifiers_to_neglect:
                        for term, info in terms.items():
                            if "compound" in info.keys():
                                if info["function"] == "head" and info["compound"] not in compounds_to_neglect:
                                    lemma = info["compound"].lower()
                                    compound = correct_spelling(lemma)
                                    #print(compound)
                                    if participant in dpas:
                                        dpa.append(compound)
                                    else:
                                        ipa.append(compound)

    compound_d["direct participants"] = dpa
    compound_d["indirect participants"] = ipa

    if verbose:
        print(f"extracted {len(dpa)+len(ipa)} compounds")
    return compound_d
