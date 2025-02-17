from collections import defaultdict, Counter
import glob
import json
import collections
import pprint

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

def construction_type(pos, lemma, info):
    """determine the construction type:
    clause, nominalization, regular noun, compound or named event"""
    if (info["article"]["lemma"] == "het" or info["article"]["lemma"] == "the") \
        and (lemma.endswith("en") or lemma.endswith("ing")):
        typ = "nominalization"
    elif pos == "PROPN":
        typ = "named event"
    elif "compound" in info.keys():
        typ = "compound"
    elif pos == "VERB":
        typ = "clause"
    elif pos == "NOUN": #\
        #and (info["article"]["lemma"] == "het" or info["article"]["lemma"] == "the") :
        typ = "regular noun"
    else:
        typ = "other"
    return typ

def info_incident(condition, time_buckets, incident, output_folder, language, verbose=0):
    """extract information about participant per time bucket"""
    incident_info = {}

    for time_bucket in time_buckets.keys():
        incident_info[time_bucket] = defaultdict(list)

    if language == None:
        for folder in glob.glob(f"{output_folder}/corpus/*"):
            for filename in glob.glob(f"{folder}/*"):
                with open(filename, 'r') as infile:
                    json_dict = json.load(infile) #open doc
                title = "".join([key for key, value in json_dict.items()]) #get title
            #    print(title)
                historical_distance = json_dict[title]["historical distance"] #get historical distance
                for bucket, rang in time_buckets.items():
                    if historical_distance in rang: #in which time bucket does this doc belong?
                        incident_info[bucket]["titles"].append(title)
                        if condition == "all":
                            terms_d = compile_terms(json_dict[title])
                            for target, info in terms_d.items():
                                if "frame" in info.keys() and "lemma" in info.keys():
                                    if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                        frame = "MH17"
                                        pos = "PROPN"
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                        frame = "Eurovision"
                                        pos = "PROPN"
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif info["frame"] != None:
                                        frame = info["frame"][0]
                                        sentence = info["sentence"]
                                        pos = info["POS"]
                                        lemma = info["lemma"]
                                        lu = f"{lemma}.{pos}".lower()
                                        if "compound" in info.keys():
                                            lemma = info["compound"]
                                            corrected_lemma = correct_spelling(lemma)
                                            lu = f"{corrected_lemma}.noun".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    else:
                                        continue
                        elif condition == "anchor":
                            if incident in json_dict[title]["frames/links"].keys():
                                for target, info in json_dict[title]["frames/links"][incident].items():
                                    if "frame" in info.keys() and "lemma" in info.keys():
                                        if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                            frame = "MH17"
                                            pos = info["POS"]
                                            lemma = info["lemma"]
                                            sentence = info["sentence"]
                                            lu = f"{lemma}.propn".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                            frame = "Eurovision"
                                            pos = "PROPN"
                                            lemma = info["lemma"]
                                            sentence = info["sentence"]
                                            lu = f"{lemma}.propn".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        elif info["frame"] != None:
                                            frame = info["frame"][0]
                                            sentence = info["sentence"]
                                            pos = info["POS"]
                                            lemma = info["lemma"]
                                            lu = f"{lemma}.{pos}".lower()
                                            if "compound" in info.keys():
                                                lemma = info["compound"]
                                                corrected_lemma = correct_spelling(lemma)
                                                lu = f"{corrected_lemma}.noun".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        else:
                                            continue
                        else:
                            if "subevents" in json_dict[title].keys():
                                for target, info in json_dict[title]["subevents"].items():
                                    if "frame" in info.keys() and "lemma" in info.keys():
                                        if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                            frame = "MH17"
                                            pos = info["POS"]
                                            lemma = info["lemma"]
                                            sentence = info["sentence"]
                                            lu = f"{lemma}.propn".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                            frame = "Eurovision"
                                            pos = "PROPN"
                                            lemma = info["lemma"]
                                            sentence = info["sentence"]
                                            lu = f"{lemma}.propn".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        elif info["frame"] != None:
                                            frame = info["frame"][0]
                                            sentence = info["sentence"]
                                            pos = info["POS"]
                                            lemma = info["lemma"]
                                            lu = f"{lemma}.{pos}".lower()
                                            if "compound" in info.keys():
                                                lemma = info["compound"]
                                                corrected_lemma = correct_spelling(lemma)
                                                lu = f"{corrected_lemma}.noun".lower()
                                            construction = construction_type(pos, lemma, info)
                                            incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                            incident_info[bucket]["frames"].append(frame)
                                            incident_info[bucket]["POS"].append(pos)
                                            incident_info[bucket]["lexical units"].append(lu)
                                        else:
                                            continue

    else:
        for filename in glob.glob(f"{output_folder}/corpus/{language}/*"):
            with open(filename, 'r') as infile:
                json_dict = json.load(infile)
            title = "".join([key for key, value in json_dict.items()]) #get title
        #    print(title)
            historical_distance = json_dict[title]["historical distance"] #get historical distance
            for bucket, rang in time_buckets.items():
                if historical_distance in rang: #in which time bucket does this doc belong?
                    incident_info[bucket]["titles"].append(title)
                    if condition == "all":
                        terms_d = compile_terms(json_dict[title])
                        for target, info in terms_d.items():
                            if "frame" in info.keys() and "lemma" in info.keys():
                                if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                    frame = "MH17"
                                    pos = info["POS"]
                                    lemma = info["lemma"]
                                    sentence = info["sentence"]
                                    lu = f"{lemma}.propn".lower()
                                    construction = construction_type(pos, lemma, info)
                                    incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                    incident_info[bucket]["frames"].append(frame)
                                    incident_info[bucket]["POS"].append(pos)
                                    incident_info[bucket]["lexical units"].append(lu)
                                elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                    frame = "Eurovision"
                                    pos = "PROPN"
                                    lemma = info["lemma"]
                                    sentence = info["sentence"]
                                    lu = f"{lemma}.propn".lower()
                                    construction = construction_type(pos, lemma, info)
                                    incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                    incident_info[bucket]["frames"].append(frame)
                                    incident_info[bucket]["POS"].append(pos)
                                    incident_info[bucket]["lexical units"].append(lu)
                                elif info["frame"] != None:
                                    frame = info["frame"][0]
                                    sentence = info["sentence"]
                                    pos = info["POS"]
                                    lemma = info["lemma"]
                                    lu = f"{lemma}.{pos}".lower()
                                    if "compound" in info.keys():
                                        lemma = info["compound"]
                                        corrected_lemma = correct_spelling(lemma)
                                        lu = f"{corrected_lemma}.noun".lower()
                                    construction = construction_type(pos, lemma, info)
                                    incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                    incident_info[bucket]["frames"].append(frame)
                                    incident_info[bucket]["POS"].append(pos)
                                    incident_info[bucket]["lexical units"].append(lu)
                                else:
                                    continue
                    elif condition == "anchor":
                        if incident in json_dict[title]["frames/links"].keys():
                            for target, info in json_dict[title]["frames/links"][incident].items():
                                if "frame" in info.keys() and "lemma" in info.keys():
                                    if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                        frame = "MH17"
                                        pos = info["POS"]
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                        frame = "Eurovision"
                                        pos = "PROPN"
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif info["frame"] != None:
                                        frame = info["frame"][0]
                                        sentence = info["sentence"]
                                        pos = info["POS"]
                                        lemma = info["lemma"]
                                        lu = f"{lemma}.{pos}".lower()
                                        if "compound" in info.keys():
                                            lemma = info["compound"]
                                            corrected_lemma = correct_spelling(lemma)
                                            lu = f"{corrected_lemma}.noun".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    else:
                                        continue
                    else:
                        if "subevents" in json_dict[title].keys():
                            for target, info in json_dict[title]["subevents"].items():
                                if "frame" in info.keys() and "lemma" in info.keys():
                                    if (info["lemma"] == "mh17" or info["lemma"] == "MH17") or (info["frame"] == "mh17" or info["frame"] == "MH17"):
                                        frame = "MH17"
                                        pos = info["POS"]
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif (info["lemma"] == "Eurovision" or info["lemma"] == "ESC") or (info["frame"] == "Eurovision" or info["frame"] == "ESC"):
                                        frame = "Eurovision"
                                        pos = "PROPN"
                                        lemma = info["lemma"]
                                        sentence = info["sentence"]
                                        lu = f"{lemma}.propn".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    elif info["frame"] != None:
                                        frame = info["frame"][0]
                                        sentence = info["sentence"]
                                        pos = info["POS"]
                                        lemma = info["lemma"]
                                        lu = f"{lemma}.{pos}".lower()
                                        if "compound" in info.keys():
                                            lemma = info["compound"]
                                            corrected_lemma = correct_spelling(lemma)
                                            lu = f"{corrected_lemma}.noun".lower()
                                        construction = construction_type(pos, lemma, info)
                                        incident_info[bucket]["joint"].append((frame, lu, pos, sentence, construction))
                                        incident_info[bucket]["frames"].append(frame)
                                        incident_info[bucket]["POS"].append(pos)
                                        incident_info[bucket]["lexical units"].append(lu)
                                    else:
                                        continue
    return incident_info

def extract_info(incident_info):
    "extract and print descriptive statistics"
    for condition, buckets in incident_info.items():
        frames = []
        lus = []
        for bucket, info in buckets.items():
            for frame in info["frames"]:
                frames.append(frame)
            for lu in info["lexical units"]:
                lus.append(lu)
        print(condition)
        print("frames:", len(frames))
        print("LUs:", len(lus))
        counter = Counter(frames)
        most_common = counter.most_common(3)
        for tupl in most_common:
            frame = tupl[0]
            freq = tupl[1]
            perc = round((freq*100)/len(frames), 1)
            print(frame, freq, f"({perc}%)")
        print()
    return

def extract_compounds(dpas, output_folder, identifiers_to_neglect, compounds_to_neglect, verbose):
    """extract all compounds from dutch corpus"""
    compound_d = {}
    dpa = []
    ipa = []

    for folder in glob.glob(f"{output_folder}/*"):
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
