import os
from lxml import etree
from collections import defaultdict, Counter
import nltk
nltk.download('framenet_v17')
from nltk.corpus import framenet as fn
import glob
import json
import collections
import pandas as pd

def check_if_annotated(root, language):
    """check if the NAF file is annotated"""
    sources = set()

    if language == "en":
        if not root.find('srl'):
            return False
        else:
            for predicate in root.find('srl'):
                ext_ref_el = predicate.findall('externalReferences/externalRef')
                source = ext_ref_el[-1].get('source')
                if source != "open-sesame":
                    sources.add(source)
            if len(sources) == 0:
                return False
            else:
                return True
    else:
        if not root.find('srl'):
            return False
        else:
            return True

def get_title(root):
    """extract text title from NAF"""
    target = root.find('nafHeader/fileDesc')
    title = target.get('title')
    return title

def get_raw_text(root):
    """extract raw layer from NAF"""
    raw = root.find('raw')
    raw_text = raw.text
    return raw_text

def return_target_or_mw(root, target_id, verbose):
    """take target_id and check in terms layer if it belongs to a multi-word. If so, return multiword id"""
    for term in root.find('terms'):
        if term.get('id') == target_id and term.get('component_of'):
            mw_id = term.get('component_of')
            if verbose >=3:
                print(f"traded {target_id} for {mw_id}")
            return mw_id
        else:
            return target_id

def get_entity_links(root, verbose):
    """load NAF file, extract coreference links and add them to a dictionary"""
    coref_dict = defaultdict(list)

    #assert root.find('coreferences'), "no coreferences layer"
    if root.find('coreferences'):
        for reference in root.find('coreferences'):
            status = reference.get('status')
            if status != "deprecated":
                ext_ref_el = reference.find('externalReferences/externalRef')
                referent = ext_ref_el.get('reference')
                type = ext_ref_el.get('reftype')
                targets = reference.findall('span/target')
                target_list = []
                for target in targets:
                    target_id = target.get('id')
                    new_target_id = return_target_or_mw(root, target_id, verbose)
                    if new_target_id not in target_list:
                        target_list.append(new_target_id)
                coref_dict[referent].append(target_list)
    return coref_dict

def get_frames(root):
    """Load a NAF file, extract the frames and their corresponding identifiers and add them to a dictionary."""
    framedict = {}

    assert root.find('srl'), "no srl layer"

    for predicate in root.find('srl'):
        status = predicate.get('status')
        pr_id = predicate.get('id')
        if status != "deprecated":
            ext_ref_el = predicate.findall('externalReferences/externalRef')
            source = ext_ref_el[-1].get('source')
            if source != "open-sesame":
                uri = ext_ref_el[-1].get('reference')
                frame = uri[35:]
                label = frame[0].upper() + frame[1:]
                target = predicate.find('span/target')
                xid = target.get('id')
                framedict[xid] = (label, pr_id)
    return framedict

def get_reftype(root):
    """extract reftype per frame"""
    reftype_dict = {}

    assert root.find('srl'), "no srl layer"

    for predicate in root.find('srl'):
        ext_ref_el = predicate.findall('externalReferences/externalRef')
        uri = ext_ref_el[-1].get('reference')
        reftype = ext_ref_el[-1].get('reftype')
        target = predicate.find('span/target')
        xid = target.get('id')
        reftype_dict[xid] = reftype
    return reftype_dict

def get_frame_elements(root):
    """load a NAF file, extract the frame elements, the corresponding identifiers and frames,
    and add them to a dictionary"""
    fes_to_remove = {"Rebellion@Current_order", "Rebellion@Current_leadership"}
    fe_dict = defaultdict(list)

    for predicate in root.find('srl'):
        status = predicate.get('status')
        pr_id = predicate.get('id')
        if status != "deprecated":
            ext_ref_el = predicate.findall('externalReferences/externalRef')
            uri = ext_ref_el[-1].get('reference')
            frame = uri[35:]
            roles = predicate.findall('role')
            for role in roles:
                ext_ref_el = role.find('externalReferences/externalRef')
                if role.get('status') == 'manual':
                    uri = ext_ref_el.get('reference')
                    if len(uri) == 0:
                        continue
                    frame_el = uri[35:]
                    split_labels = frame_el.split('@')
                    if split_labels[0] != frame:
                        continue
                    split_upper = [split_labels[0][0].upper() + split_labels[0][1:],
                                    split_labels[1][0].upper() + split_labels[1][1:]]
                    frame_fe = '@'.join(split_upper)
                    if role.find('span'):
                        target = role.find('span/target')
                        idx = target.get('id')
                        fe_dict[idx].append((frame_fe, pr_id)) #add the frame's predicate id
                    else:
                        fe_dict['implicated'].append((frame_fe, pr_id))
    return fe_dict

def get_deps(root, target):
    """reconstruct the universal dependencies of the target in the deps layer"""
    deps = []

    deps.append(target)

    for dep in root.find('deps'):
        if dep.get('from') == target:
            dep1 = dep.get('to')
            deps.append(dep1)
            for dep in root.find('deps'):
                if dep.get('from') == dep1:
                    dep2 = dep.get('to')
                    deps.append(dep2)
                    for dep in root.find('deps'):
                        if dep.get('from') == dep2:
                            dep3 = dep.get('to')
                            deps.append(dep3)
    return deps

def reconstruct_multiwords(mw_id, term_id):
    """check in the dict of phrasal heads and return dictionary with phrasal verb info"""
    phrasal_heads = {"mw1": {"t5": {"lemma": "neerschieten" ,"POS": "VERB", "wf": "w5"}}}

    if mw_id in phrasal_heads.keys():
        if term_id in phrasal_heads[mw_id].keys():
            reconstructed_lemmapos = phrasal_heads[mw_id][term_id]
        else:
            reconstructed_lemmapos = "phrasal particle"
    else:
        reconstructed_lemmapos = False
    return reconstructed_lemmapos

def get_lemmas(root):
    """load a NAF file, extract the term id and corresponding lemma, POS and wf and add them to a dictionary."""
    lemma_dict = {}

    assert root.find('terms'), "no terms layer"

    for term in root.find('terms'):
        if term.get('component_of'):
            mw_id = term.get('component_of')
            term_id = term.get('id')
            if root.find('multiwords'):
                for mw in root.find('multiwords'):
                    if mw.get('id') == mw_id:
                        mw_id = mw.get('id')
                        lemma = mw.get('lemma')
                        pos = mw.get('pos')
                        target = term.find('span/target')
                        target_id = target.get('id')
                        lemmapos = {"lemma": lemma, "POS": pos, "wf": target_id}
                        lemma_dict[mw_id] = lemmapos
            else:
                reconstructed_lemmapos = reconstruct_multiwords(mw_id, term_id)
                assert type(reconstructed_lemmapos) == dict or type(reconstructed_lemmapos) == str, "multiwords in terms, but no multiwords layer"
                if type(reconstructed_lemmapos) == str:
                    continue
                else:
                    lemma_dict[mw_id] = reconstructed_lemmapos
        else:
            term_id = term.get('id')
            lemma = term.get('lemma')
            pos = term.get('pos')
            target = term.find('span/target')
            target_id = target.get('id')
            lemmapos = {"lemma": lemma, "POS": pos, "wf": target_id}
            lemma_dict[term_id] = lemmapos
    return lemma_dict

def get_sentence_info(root):
    """Load a NAF file, extract the sentence ids with corresponding wfs and add them to a dictionary."""
    sentence_dict = defaultdict(list)

    assert root.find('text'), "no text layer"

    for term in root.find('text'):
        sentence = term.get('sent')
        wf = term.get('id')
        sentence_dict[sentence].append(wf)
    return sentence_dict

def get_compound_info(root, lemma_dict, language):
    """load a NAF file, extract info about compounding."""
    compound_dict = {}

    if language == "nl":
        for term in root.find('terms'):
            if term.get('compound_type'):
                compound_lemma = term.get('lemma')
                head_id = term.get('head')
                components = term.findall('component')
                for component in components:
                    idx = component.get('id')
                    pos = component.get('pos')
                    lemma = component.get('lemma')
                    term_id = idx[:-3]
                    if idx == head_id:
                        compound_dict[idx] = {"lemma": lemma,
                                             "function": 'head',
                                             "POS": pos,
                                             "compound": compound_lemma,
                                             "term id": term_id}
                    else:
                        compound_dict[idx] = {"lemma": lemma,
                                             "function": 'modifier',
                                             "POS": pos,
                                             "compound": compound_lemma,
                                             "term id": term_id}
    else:
        for term_id, info in lemma_dict.items():
            if info["POS"] == "NOUN":
                lemma = info["lemma"]
                term_int = int(term_id[1:])
                prev_term = f"t{term_int-1}"
                next_term = f"t{term_int+1}"
                if prev_term in lemma_dict.keys():
                    if lemma_dict[prev_term]["POS"] == "NOUN":
                        prev_term_lemma = lemma_dict[prev_term]["lemma"]
                        compound_dict[term_id] = {"lemma": lemma,
                                                "function": 'head',
                                                "POS": "NOUN",
                                                "compound": f"{prev_term_lemma} {lemma}",
                                                "term id": term_id}
                if next_term in lemma_dict.keys():
                    if lemma_dict[next_term]["POS"] == "NOUN":
                        next_term_lemma = lemma_dict[next_term]["lemma"]
                        compound_dict[term_id] = {"lemma": lemma,
                                                "function": 'modifier',
                                                "POS": "NOUN",
                                                "compound": f"{lemma} {next_term_lemma}",
                                                "term id": term_id}
    return compound_dict

def move_fes(fe_dict, compound_dict):
    """move relevant fes from a split compound that was corrected, to the corrected target (without suffix)"""
    for target, fes in fe_dict.copy().items():
        if ".c" in target and target not in compound_dict.keys():
            for fe in fes:
                fe_dict[target[:-3]].append(fe)
            del fe_dict[target]
    return

def remove_deprecated_mws(frames_dict, lemma_dict, fe_dict):
    """remove deprecated multiwords from frames_dict or fe_dict"""
    for target, frame in frames_dict.copy().items():
        if target.startswith('mw') and target not in lemma_dict.keys():
            del frames_dict[target]
    for target, fe in fe_dict.copy().items():
        if target.startswith('mw') and target not in lemma_dict.keys():
            del fe_dict[target]
    return

def get_determiner_info(root):
    """load a NAF file, extract info about determiners"""
    detdict = {}

    if root.find('deps') in root:
        for dep in root.find('deps'):
            if dep.get('rfunc') == "det":
                det_id = dep.get("to")
                predicate_id = dep.get("from")
                detdict[predicate_id] = {"det id": det_id}
    return detdict

def deps(root):
    """load a NAF file, extract deps layer"""
    deps_dict = {}

    if root.find('deps') in root:
        for dep in root.find('deps'):
            term_id = dep.get('to')
            function = dep.get('rfunc')
            deps_dict[term_id] = function
    return deps_dict

def doc_hdd(title, hdd_list):
    """return historical distance given a document title"""
    for doc in hdd_list:
        if doc["title"] == title:
            historical_distance = doc['historical distance']
    return historical_distance

def check_mention_mh17(token, lemma_dict, compound_dict):
    """check for a token if it denotes 'MH17'"""
    if token in lemma_dict.keys():
        if lemma_dict[token]["lemma"] == "mh17" or lemma_dict[token]["lemma"] == "MH17":
            return True
        else:
            return False

    if token in compound_dict.keys():
        if compound_dict[token]["lemma"] == "mh17" or compound_dict[token]["lemma"] == "MH17":
            return True
        else:
            return False
    else:
        return False

def check_mention_eurovision(token, lemma_dict, compound_dict):
    """check for a token if it denotes 'Eurovision'"""
    if token in lemma_dict.keys():
        if lemma_dict[token]["lemma"] == "Eurovision" or lemma_dict[token]["lemma"] == "ESC":
            return True
        else:
            return False

    if token in compound_dict.keys():
        if compound_dict[token]["lemma"] == "Eurovision" or compound_dict[token]["lemma"] == "ESC":
            return True
        else:
            return False
    else:
        return False

def add_unexpressed_coresets(frames_dict, fe_dict, verbose):
    "find unannotated frame elements from a core set and add them as implicated"
    for target, tupl in frames_dict.items(): #iterate over frames
        frame_label = tupl[0]
        frame_predicate = tupl[1] #get frame pred
        fn_frame = fn.frame(frame_label) #iterate over FrameNet NLTK
        if len(fn_frame.FEcoreSets) != 0: #check if frame has core set
            annotated_fes = []
            for target, lst in fe_dict.copy().items(): #iterate over fe_dict
                for tupl in lst:
                    fe_predicate = tupl[1]
                    if fe_predicate == frame_predicate:
                        fe = tupl[0]
                        annotated_fes.append(fe) #add annotated fe's to set
            for coreset in fn_frame.FEcoreSets: #iterate over coresets
                new_coreset = []
                for core_fe in coreset: #iterate over fe's in coreset
                    label = core_fe.name
                    new_label = f"{frame_label}@{label}"
                    new_coreset.append(new_label) #append newly labeled fe's to list
                if any(i in new_coreset for i in annotated_fes): #if any of the fe's in coreset are in the annotated set
                    for new_label_fe in new_coreset: #iterate over the coreset
                        if new_label_fe not in annotated_fes: #if fe not in annotated list
                            new_fe_pred = (new_label_fe, frame_predicate)
                            fe_dict["implicated"].append(new_fe_pred) #append unannotated coreset fe to fe_dict
                            if verbose >= 3:
                                print(f"added {new_fe_pred} as implicated")
    return

def check_attendee_fe(frames_dict,fe_dict, verbose):
    """add Attendee as implicated"""
    for target, tupl in frames_dict.items(): #iterate over frames
        if tupl[0] == "Social_event":
            frame_label = tupl[0]
            frame_predicate = tupl[1] #get frame pred
            annotated_fes = []
            for target, lst in fe_dict.copy().items(): #iterate over fe_dict
                for tupl in lst:
                    if tupl[1] == frame_predicate:
                        fe = tupl[0]
                        annotated_fes.append(fe) #add annotated fe's to set
            if "Social_event@Attendee" not in annotated_fes:
                new_fe_pred = ("Social_event@Attendee", frame_predicate)
                fe_dict["implicated"].append(new_fe_pred) #append unannotated fe to fe_dict
                if verbose >= 3:
                    print(f"added {new_fe_pred} as implicated")
    return

def get_subevents(entity_links_dict, frames_dict, lemma_dict, sentence_dict, compound_dict, det_dict, fe_dict, deps_dict):
    """create a dictionary for frames without coreference"""
    subevents_dict = {}
    coref_targets = []

    for identifier, spans in entity_links_dict.items():
        for span in spans:
            for target in span:
                coref_targets.append(target)

    for target, label in frames_dict.items():
        if target not in coref_targets:
            info = {}
            info['frame'] = label
            if target in fe_dict:
                fes = fe_dict[target]
                info['frame elements'] = fes
            else:
                info['frame elements'] = None
            for token, term_info in lemma_dict.items():
                if token == target:
                    lemma = term_info['lemma']
                    pos = term_info['POS']
                    wf = term_info['wf']
                    info['lemma'] = lemma
                    info['POS'] = pos
                    for sentence, wfs in sentence_dict.items():
                        if wf in wfs:
                            info['sentence'] = int(sentence)
                            weighted_token_occ = 1/int(sentence)
                            info['discourse ratio'] = round(weighted_token_occ, 3)
                            token_index = wfs.index(wf)
                            if token_index == 0:
                                token_index = 1
                            weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                            info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            for token, compound_info in compound_dict.items():
                if token == target:
                    lemma = compound_info['lemma']
                    pos = compound_info['POS']
                    compound = compound_info['compound']
                    function = compound_info['function']
                    term_id = compound_info['term id']
                    if function == "head" and term_id in deps_dict:
                        dep = deps_dict[term_id]
                        info['syntactic relation'] = dep
                    info['lemma'] = lemma
                    info['POS'] = pos
                    info['compound'] = compound
                    info['function'] = function
                    for term, term_info in lemma_dict.items():
                        if term == term_id:
                            wf = term_info['wf']
                            for sentence, wfs in sentence_dict.items():
                                if wf in wfs:
                                    info['sentence'] = int(sentence)
                                    weighted_token_occ = 1/int(sentence)
                                    info['discourse ratio'] = round(weighted_token_occ, 3)
                                    token_index = wfs.index(wf)
                                    if token_index == 0:
                                        token_index = 1
                                    weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                                    info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            if target in det_dict:
                det_id = det_dict[target]['det id']
                if det_id in lemma_dict and (lemma_dict[det_id]['lemma'] == 'een' or lemma_dict[det_id]['lemma'] == 'het' or lemma_dict[det_id]['lemma'] == 'de'):
                    article = lemma_dict[det_id]['lemma']
                    if article == 'de' or article == 'het':
                        definite_dict = {"definite": True, "lemma": article}
                        info['article'] = definite_dict
                    else:
                        definite_dict = {"definite": False, "lemma": article}
                        info['article'] = definite_dict
                else:
                    info['article'] = {"definite": None, "lemma": None}
            else:
                info['article'] = {"definite": None, "lemma": None}
            if target in deps_dict:
                dep = deps_dict[target]
                info['syntactic relation'] = dep
            if "lemma" in info.keys():
                subevents_dict[target] = info
            else:
                continue

    for target, info in subevents_dict.items():
        if "syntactic relation" not in info:
            info["syntactic relation"] = None
    return subevents_dict

def get_fes_without_link(entity_links_dict, frames_dict, lemma_dict, sentence_dict, compound_dict, det_dict, fe_dict, deps_dict):
    """create dictionary for frame elements without coreference"""
    fes_without_link_dict = {}
    coref_targets = []

    for identifier, spans in entity_links_dict.items():
        for span in spans:
            for target in span:
                coref_targets.append(target)

    for target, fes in fe_dict.items():
        if target not in coref_targets and target not in frames_dict and target != "implicated":
            info = {}
            info['frame elements'] = fes
            for token, term_info in lemma_dict.items():
                if token == target:
                    lemma = term_info['lemma']
                    pos = term_info['POS']
                    wf = term_info['wf']
                    info['lemma'] = lemma
                    info['POS'] = pos
                    for sentence, wfs in sentence_dict.items():
                        if wf in wfs:
                            info['sentence'] = int(sentence)
                            weighted_token_occ = 1/int(sentence)
                            info['discourse ratio'] = round(weighted_token_occ, 3)
                            token_index = wfs.index(wf)
                            if token_index == 0:
                                token_index = 1
                            weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                            info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            for token, compound_info in compound_dict.items():
                if token == target:
                    lemma = compound_info['lemma']
                    pos = compound_info['POS']
                    compound = compound_info['compound']
                    function = compound_info['function']
                    term_id = compound_info['term id']
                    if function == "head" and term_id in deps_dict:
                        dep = deps_dict[term_id]
                        info['syntactic relation'] = dep
                    info['lemma'] = lemma
                    info['POS'] = pos
                    info['compound'] = compound
                    info['function'] = function
                    for term, term_info in lemma_dict.items():
                        if term == term_id:
                            wf = term_info['wf']
                            for sentence, wfs in sentence_dict.items():
                                if wf in wfs:
                                    info['sentence'] = int(sentence)
                                    weighted_token_occ = 1/int(sentence)
                                    info['discourse ratio'] = round(weighted_token_occ, 3)
                                    token_index = wfs.index(wf)
                                    if token_index == 0:
                                        token_index = 1
                                    weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                                    info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            if target in det_dict:
                det_id = det_dict[target]['det id']
                if det_id in lemma_dict and (lemma_dict[det_id]['lemma'] == 'een' or lemma_dict[det_id]['lemma'] == 'het' or lemma_dict[det_id]['lemma'] == 'de'):
                    article = lemma_dict[det_id]['lemma']
                    if article == 'de' or article == 'het':
                        definite_dict = {"definite": True, "lemma": article}
                        info['article'] = definite_dict
                    else:
                        definite_dict = {"definite": False, "lemma": article}
                        info['article'] = definite_dict
                else:
                    info['article'] = {"definite": None, "lemma": None}
            else:
                info['article'] = {"definite": None, "lemma": None}
            if target in deps_dict:
                dep = deps_dict[target]
                info['syntactic relation'] = dep
            fes_without_link_dict[target] = info

    for target, info in fes_without_link_dict.items():
        if "syntactic relation" not in info:
            info["syntactic relation"] = None
    return fes_without_link_dict

def doc_variation(title,
                    entity_links_dict,
                    frames_dict,
                    fe_dict,
                    lemma_dict,
                    sentence_dict,
                    det_dict,
                    compound_dict,
                    deps_dict,
                    hdd_list,
                    raw_text,
                    root):
    """integrate different dictionaries extracted from naf in order to create a frame_info_dict"""
    variation_dict = defaultdict(dict)
    fes_without_link = {}

    for entity, ids in entity_links_dict.items():
        target_dict = {}
        for span in ids:
            for token in span:
                token_dict = {}
                for target, label in frames_dict.items():
                    if target == token:
                        token_dict["frame"] = label
                for target, fes in fe_dict.items():
                    if target == token:
                        token_dict["frame elements"] = fes
                if entity == "Q17374096" and check_mention_mh17(token, lemma_dict, compound_dict) == True and len(token_dict) == 0:
                    token_dict["frame"] = "MH17"
                    token_dict["frame elements"] = None
                if entity == "Q30973589" and check_mention_eurovision(token, lemma_dict, compound_dict) == True and len(token_dict) == 0:
                    token_dict["frame"] = "Eurovision"
                    token_dict["frame elements"] = None
                target_dict[token] = token_dict
                if "frame" not in token_dict.keys():
                    token_dict["frame"] = None
                if "frame elements" not in token_dict.keys():
                    token_dict["frame elements"] = None
        for key in list(target_dict.keys()):
            values = list(target_dict[key].values())
            if len(values) == 2:
                if values[0] == None and values[1] == None:
                    del target_dict[key]
            else:
                continue
        variation_dict[entity] = target_dict

    for entity, targets in variation_dict.items():
        for target, info in targets.items():
            for token, term_info in lemma_dict.items():
                if token == target:
                    lemma = term_info['lemma']
                    pos = term_info['POS']
                    wf = term_info['wf']
                    info['lemma'] = lemma
                    info['POS'] = pos
                    for sentence, wfs in sentence_dict.items():
                        if wf in wfs:
                            info['sentence'] = int(sentence)
                            weighted_token_occ = 1/int(sentence)
                            info['discourse ratio'] = round(weighted_token_occ, 3)
                            token_index = wfs.index(wf)
                            if token_index == 0:
                                token_index = 1
                            weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                            info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            for token, compound_info in compound_dict.items():
                if token == target:
                    lemma = compound_info['lemma']
                    pos = compound_info['POS']
                    compound = compound_info['compound']
                    function = compound_info['function']
                    term_id = compound_info['term id']
                    if function == "head" and term_id in deps_dict:
                        dep = deps_dict[term_id]
                        info['syntactic relation'] = dep
                    info['lemma'] = lemma
                    info['POS'] = pos
                    info['compound'] = compound
                    info['function'] = function
                    for term, term_info in lemma_dict.items():
                        if term == term_id:
                            wf = term_info['wf']
                            for sentence, wfs in sentence_dict.items():
                                if wf in wfs:
                                    info['sentence'] = int(sentence)
                                    weighted_token_occ = 1/int(sentence)
                                    info['discourse ratio'] = round(weighted_token_occ, 3)
                                    token_index = wfs.index(wf)
                                    if token_index == 0:
                                        token_index = 1
                                    weighted_token_occ_discourse_sentence = 1/(int(sentence)**2 * token_index)
                                    info['discourse_sentence sensitivity'] = round(weighted_token_occ_discourse_sentence, 3)
            if target in det_dict:
                det_id = det_dict[target]['det id']
                if det_id in lemma_dict and (lemma_dict[det_id]['lemma'] == 'een' or lemma_dict[det_id]['lemma'] == 'het' or lemma_dict[det_id]['lemma'] == 'de'):
                    article = lemma_dict[det_id]['lemma']
                    if article == 'de' or article == 'het':
                        definite_dict = {"definite": True, "lemma": article}
                        info['article'] = definite_dict
                    else:
                        definite_dict = {"definite": False, "lemma": article}
                        info['article'] = definite_dict
                else:
                    info['article'] = {"definite": None, "lemma": None}
            else:
                info['article'] = {"definite": None, "lemma": None}
            if target in deps_dict:
                dep = deps_dict[target]
                info['syntactic relation'] = dep

    for wiki_id, target_d in variation_dict.items():
        for target, info_d in target_d.items():
            if "syntactic relation" not in info_d:
                info_d["syntactic relation"] = None
            if info_d["frame elements"] != None and "compound" not in info_d:
                lemmas_l = []
                deps = get_deps(root, target)
                sorted_deps = sorted(deps)
                for dep in sorted_deps:
                    for lemma_target, lemma_info_d in lemma_dict.items():
                        if lemma_target == dep:
                            lemma = lemma_info_d['lemma']
                            lemmas_l.append(lemma)
                phrase = ' '.join(lemmas_l)
                info_d["target phrase"] = phrase
            elif info_d["frame elements"] != None and "compound" in info_d:
                compound = info_d["compound"]
                info_d["target phrase"] = compound
            else:
                continue

    reftype_dict = get_reftype(root)

    for entity, targets in variation_dict.items():
        for target, info in targets.items():
            for token, reftype in reftype_dict.items():
                if token == target:
                    info['reftype'] = reftype

    historical_distance = doc_hdd(title, hdd_list)
    subevents_dict = get_subevents(entity_links_dict, frames_dict, lemma_dict, sentence_dict, compound_dict, det_dict, fe_dict, deps_dict)
    fes_without_link_dict = get_fes_without_link(entity_links_dict, frames_dict, lemma_dict, sentence_dict, compound_dict, det_dict, fe_dict, deps_dict)

    for target, info_d in subevents_dict.items():
        for token, reftype in reftype_dict.items():
            if token == target:
                info_d['reftype'] = reftype
        if info_d["frame elements"] != None and "compound" not in info_d:
            lemmas_l = []
            deps = get_deps(root, target)
            sorted_deps = sorted(deps)
            for dep in sorted_deps:
                for lemma_target, lemma_info_d in lemma_dict.items():
                    if lemma_target == dep:
                        lemma = lemma_info_d['lemma']
                        lemmas_l.append(lemma)
            phrase = ' '.join(lemmas_l)
            info_d["target phrase"] = phrase
        elif info_d["frame elements"] != None and "compound" in info_d:
            compound = info_d["compound"]
            info_d["target phrase"] = compound
        else:
            continue

    for target, info_d in fes_without_link_dict.items():
        for token, reftype in reftype_dict.items():
            if token == target:
                info_d['reftype'] = reftype
        if info_d["frame elements"] != None and "compound" not in info_d:
            lemmas_l = []
            deps = get_deps(root, target)
            sorted_deps = sorted(deps)
            for dep in sorted_deps:
                for lemma_target, lemma_info_d in lemma_dict.items():
                    if lemma_target == dep:
                        lemma = lemma_info_d['lemma']
                        lemmas_l.append(lemma)
            phrase = ' '.join(lemmas_l)
            info_d["target phrase"] = phrase
        elif info_d["frame elements"] != None and "compound" in info_d:
            compound = info_d["compound"]
            info_d["target phrase"] = compound
        else:
            continue

    #for wiki_id, target_d in variation_dict.copy().items():
    #    for target, info_d in target_d.items():
    #        if 'sentence' not in info_d.keys():
    #            del target_d[target]
    #for target, info_d in subevents_dict.copy().items():
    #    if 'sentence' not in info_d.keys():
    #        del subevents_dict[target]
    #for target, info_d in fes_without_link_dict.copy().items():
    #    if 'sentence' not in info_d.keys():
    #        del fes_without_link_dict[target]



    doc_variation_dict = {title: {"raw text": raw_text,
                                    "frames/links": variation_dict,
                                    "implicated fe's": fe_dict['implicated'],
                                    "subevents": subevents_dict,
                                    "fe's without links": fes_without_link_dict,
                                    "historical distance": historical_distance}}
    return doc_variation_dict

def descriptive_stats(language, title, incident, entity_links_dict, frames_dict, fe_dict, subevents_dict):
    """return the following information for a document: number of entity-links, number of lexical units, number of frame elements"""
    entity_links = []
    lus = []
    fes = []

    for identifier, spans in entity_links_dict.items():
        for span in spans:
            entity_links.append(span)
    if subevents_dict != None:
        for list_of_tupls in subevents_dict[incident][language][title]:
            for tupl in list_of_tupls:
                target = tupl[0]
                entity_links.append(target)

    for target, frame in frames_dict.items():
        lus.append(target)

    for target, lst in fe_dict.items():
        for tupl in lst:
            fe = tupl[0]
            fes.append(target)
    return entity_links, lus, fes

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
    if "frame" in info_d.keys():
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

def descriptive_fe_stats(incident, language):
    fes_to_remove = {"Rebellion@Current_order", "Rebellion@Current_leadership"}
    exclude_fes = ["Cause_harm@Cause",
                "Violence@Aggressors",
                "Violence@Cause"]
    word = []
    sentence = []
    discourse = []
    unexpressed = []

    for filename in glob.glob(f"../output/{incident}/corpus/{language}/*"):
        with open(filename, 'r') as infile:
            json_dict = json.load(infile)
        title = "".join([key for key, value in json_dict.items()])
        #print(title)
        terms_d = compile_terms(json_dict[title])
        for term, info in terms_d.items():
            if "sentence" in info.keys():
                fe_sentence = info["sentence"]
                if info["frame elements"] != None:
                    for tupl in info["frame elements"]:
                        fe = tupl[0]
                        fe_pred = tupl[1]
                        if fe in fes_to_remove:
                            continue
                        else:
                            if check_interface_status(info, terms_d, fe_pred, fe_sentence) == "word":
                                word.append(fe)
                            elif check_interface_status(info, terms_d, fe_pred, fe_sentence) == "sentence":
                                sentence.append(fe)
                            else:
                                discourse.append(fe)
        for tupl in json_dict[title]["implicated fe's"]:
            fe = tupl[0]
            pred_id = tupl[1]
            if fe in exclude_fes:
                continue
            else:
                unexpressed.append(fe)

    all_fes = len(word) + len(sentence) + len(discourse) + len(unexpressed)
    fe_freq_l = [len(word), len(sentence), len(discourse), len(unexpressed)]
    fe_freq_perc_l = []
    for freq in fe_freq_l:
        perc = round((freq*100)/all_fes, 2)
        fe_freq_perc_l.append((freq, perc))
    return fe_freq_perc_l, all_fes
