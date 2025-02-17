from .path_utils import get_naf_paths
from .historical_distance_utils import prepare_timeline_plot, get_titles_and_publication_dates, timestamps_collection, validate_publication_date, calculate_difference
from .xml_utils import descriptive_fe_stats, check_attendee_fe, deps, check_if_annotated, get_raw_text, get_title, get_frames, get_frame_elements, get_lemmas, get_entity_links, get_sentence_info, get_compound_info, get_determiner_info, doc_variation, move_fes, remove_deprecated_mws, descriptive_stats, add_unexpressed_coresets
from .output_utils import create_output_folder, variation_to_excel
from .incident_info_utils import extract_compounds, compile_terms, info_incident, extract_info
from .validation_utils import map_subevents_to_instance
from .frame_element_analysis_utils import plot_lu_offset, lu_distribution, remove_named_events, frames_distribution, plot_figure, restructure_data, type_selection, reorder_time_buckets
from .entropy_utils import calculate_unexpressed_entropy, calculate_entropy, entropy_to_latex
from .construction_utils import plot_clustered_stacked, prepare_stacked_barplot, syntactic_function_distribution
from .participant_analysis_utils import export_unexpressed_fes, extract_compounds, get_unexpressed_fes, get_frequency_ranking_of_participants, compile_terms, check_interface_status, info_participant, extract_info, bundle_participants
from .references_utils import export_plots, prepare_plotting
from .lexical_unit_analysis_utils import compound_analysis, compounds_to_latex, top_ranked_lus, extract_pos_info, plot_pos, evokes_distribution_to_latex, evokes_distribution, head_distribution_to_latex
from .unexpressed_utils import restructure_unexpressed_data
from lxml import etree
import json
import glob
import os
import pickle
import pandas as pd
import numpy as np
import pprint
from collections import defaultdict
from matplotlib import pyplot as plt
import random

def interface_analysis(incident,
                participants_d,
                unexpressed_d,
                ordered_l,
                output_folder,
                figsize=None,
                start_from_scratch=False,
                verbose=0):
    """plot the relative number of references of the participants over time"""
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/figures/interfaces",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    data_d = prepare_plotting(participants_d=participants_d,
                                ordered_l=ordered_l,
                                dimension="discourse realizations")
    export_plots(plot_data=data_d,
                incident=incident,
                output_folder=output_folder,
                verbose=verbose)
    for participant, v in participants_d.items():
        plot_syntax_data = restructure_data(participants_d=participants_d,
                                        participant=participant,
                                        ordered_l=ordered_l,
                                        dimension="sentence realizations",
                                        verbose=verbose)
        plot_figure(plot_data=plot_syntax_data,
                    output_folder=output_folder,
                    participant=participant,
                    incident=incident,
                    verbose=verbose,
                    specified_figsize=figsize,
                    dimension="sentence realizations",
                    interfaces=True)
        plot_discourse_data = restructure_data(participants_d=participants_d,
                                        participant=participant,
                                        ordered_l=ordered_l,
                                        dimension="discourse realizations",
                                        verbose=verbose)
        plot_figure(plot_data=plot_discourse_data,
                    output_folder=output_folder,
                    participant=participant,
                    incident=incident,
                    verbose=verbose,
                    specified_figsize=figsize,
                    dimension="discourse realizations",
                    interfaces=True)
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/tables/unexpressed",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    unexpressed_anchor_data = restructure_unexpressed_data(incident_d=unexpressed_d,
                                                                condition="anchor",
                                                                ordered_l=ordered_l,
                                                                output_folder=output_folder,
                                                                incident=incident,
                                                                verbose=verbose)
    plot_figure(unexpressed_anchor_data,
                output_folder=output_folder,
                participant=None,
                incident=incident,
                verbose=verbose,
                specified_figsize=figsize,
                dimension="unexpressed",
                interfaces=True,
                unexpressed_condition="anchor")
    unexpressed_climax_data = restructure_unexpressed_data(incident_d=unexpressed_d,
                                                                condition="non-anchor",
                                                                ordered_l=ordered_l,
                                                                output_folder=output_folder,
                                                                incident=incident,
                                                                verbose=verbose)
    plot_figure(unexpressed_climax_data,
                output_folder=output_folder,
                participant=None,
                incident=incident,
                verbose=verbose,
                specified_figsize=figsize,
                dimension="unexpressed",
                interfaces=True,
                unexpressed_condition="climax")
    return

def compounds(output_folder,
                direct_participants,
                identifiers_to_neglect=set(),
                compounds_to_exclude=set(),
                exclude_fes=[],
                bundle_participants=None,
                verbose=0):
    """extract compounds per participant"""
    compound_d = extract_compounds(dpas=direct_participants,
                                    output_folder=output_folder,
                                    identifiers_to_neglect=identifiers_to_neglect,
                                    compounds_to_neglect=compounds_to_exclude,
                                    verbose=verbose)
    json_path = f"{output_folder}/output/compounds.json"
    with open(json_path, 'w') as outfile:
        json.dump(compound_d, outfile, indent=4, sort_keys=True)

    if verbose:
        print(f"exported compounds to {json_path}")
    return


def lu_analysis(incident,
                participant_d,
                ordered_l,
                output_folder,
                n_time_buckets=None,
                start_from_scratch=False,
                language=None,
                compounds=False,
                verbose=0):
    """conduct a lexical unit analysis at participant level"""
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/tables/lexical units",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/figures/lexical units",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    if language != None:
        ds = evokes_distribution(participants_d=participant_d)
        evokes_distribution_to_latex(ds=ds,
                                    incident=incident,
                                    language=language,
                                    output_folder=output_folder,
                                    verbose=verbose)
        participants_l = ["Gökmen Tanis", "pro-Russian rebels", "rioters", "participants"]
        for participant, v in participant_d.items():
            if participant in participants_l:
                ds = top_ranked_lus(participant_d=participant_d[participant])
                head_distribution_to_latex(ds=ds,
                                            incident=incident,
                                            output_folder=output_folder,
                                            participant=participant,
                                            language=language,
                                            verbose=verbose)

    elif compounds == True:
        df = compound_analysis(compounds_d=participant_d)
        compounds_to_latex(df=df,
                            output_folder=output_folder,
                            verbose=verbose)
    else:
        for participant, v in participant_d.items():
            plot_data = extract_pos_info(participants_d=participant_d,
                                            participant=participant,
                                            ordered_tbs=ordered_l)
            plot_pos(plot_data=plot_data,
                    n_columns=n_time_buckets,
                    ordered_l=ordered_l,
                    output_folder=output_folder,
                    incident=incident,
                    participant=participant,
                    verbose=verbose)

def references(incident,
                participants_d,
                ordered_l,
                output_folder,
                dimension,
                start_from_scratch=False,
                verbose=0):
    """plot the relative number of references of the participants over time"""
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/figures/references",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    data_d = prepare_plotting(participants_d=participants_d,
                                ordered_l=ordered_l,
                                dimension=dimension)
    export_plots(plot_data=data_d,
                incident=incident,
                output_folder=output_folder,
                verbose=verbose)

def derive_entropy(utrecht_d,
                    utrecht_ordered,
                    mh17_d,
                    mh17_ordered,
                    curfew_d,
                    curfew_ordered,
                    eurovision_d,
                    eurovision_ordered,
                    feature,
                    output_folder,
                    unexpressed_dicts=None,
                    verbose=0):
    """calculates the entropy values for all incidents between time buckets"""
    fe_entropy_d = {}
    utrecht_ent_d = calculate_entropy(utrecht_d, feature, utrecht_ordered)
    fe_entropy_d["Utrecht shooting"] = utrecht_ent_d
    mh17_ent_d = calculate_entropy(mh17_d, feature, mh17_ordered)
    fe_entropy_d["Malaysia Airlines flight 17"] = mh17_ent_d
    curfew_ent_d = calculate_entropy(curfew_d, feature, curfew_ordered)
    fe_entropy_d["Dutch curfew riots"] = curfew_ent_d
    eurovision_ent_d = calculate_entropy(eurovision_d, feature, eurovision_ordered)
    fe_entropy_d["Eurovsion Song Contest 2021"] = eurovision_ent_d
    if verbose >= 2:
        pprint.pprint(fe_entropy_d)

    json_path = f"{output_folder}/output/participants_{feature}_entropy.json"

    with open(json_path, 'w') as outfile:
        json.dump(fe_entropy_d, outfile, indent=4, sort_keys=True)

    if verbose:
        print(f"exported participant frame element entropy to {json_path}")

    if unexpressed_dicts != None:
        unexpressed_entropy_d = {}
        utrecht_unexpressed_ent_d = calculate_unexpressed_entropy(unexpressed_dicts[0], utrecht_ordered)
        unexpressed_entropy_d["Utrecht shooting"] = utrecht_unexpressed_ent_d
        mh17_unexpressed_ent_d = calculate_unexpressed_entropy(unexpressed_dicts[1], mh17_ordered)
        unexpressed_entropy_d["Malaysia Airlines flight 17"] = mh17_unexpressed_ent_d
        curfew_unexpresssed_ent_d = calculate_unexpressed_entropy(unexpressed_dicts[2], curfew_ordered)
        unexpressed_entropy_d["Dutch curfew riots"] = curfew_unexpresssed_ent_d
        eurovision_unexpressed_ent_d = calculate_unexpressed_entropy(unexpressed_dicts[3], eurovision_ordered)
        unexpressed_entropy_d["Eurovsion Song Contest 2021"] = eurovision_unexpressed_ent_d
        entropy_to_latex(frames_entropy_d=unexpressed_entropy_d,
                            feature="unexpressed",
                            output_folder=output_folder,
                            verbose=verbose)
    return

def construction_analysis(incident,
                            data_d,
                            ordered_l,
                            output_folder,
                            colors,
                            figsize=None,
                            start_from_scratch=False,
                            verbose=0):
    """conduct analysis of variation in constructions in reference to participants"""
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/figures/constructions",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)
    syntax_dict = syntactic_function_distribution(participants_d=data_d)
    values, participants = prepare_stacked_barplot(syntax_dict, "subject", ordered_l)
    df1 = pd.DataFrame(values,
                        index=ordered_l,
                        columns=participants)
    values, participants = prepare_stacked_barplot(syntax_dict, "other", ordered_l)
    df2 = pd.DataFrame(values,
                       index=ordered_l,
                       columns=participants)
    plot_clustered_stacked(dfall=[df1, df2],
                            colors=colors,
                            labels=["subject", "other"],
                            figsize=figsize)
    pdf_path = f"{output_folder}/output/{incident}/figures/constructions/constructions_{incident}.pdf"
    plt.savefig(pdf_path, bbox_inches='tight')
    if verbose:
        print(f"exported stacked barplot to {pdf_path}")
    return

def fe_analysis(incident,
                    data_dict,
                    ordered_time_buckets,
                    output_folder,
                    dimension,
                    figsize=None,
                    bbox_to_anchor=None,
                    start_from_scratch=False,
                    verbose=0):
    """conduct analysis of variation in frame elements in reference to participants"""
    create_output_folder(output_folder=f"{output_folder}/output/{incident}/figures/{dimension}",
                        start_from_scratch=start_from_scratch,
                        verbose=verbose)

    for participant, v in data_dict.items():
        plot_data = restructure_data(participants_d=data_dict,
                                    participant=participant,
                                    ordered_l=ordered_time_buckets,
                                    dimension=dimension,
                                    verbose=verbose)
        plot_figure(plot_data=plot_data,
                    output_folder=output_folder,
                    participant=participant,
                    incident=incident,
                    verbose=verbose,
                    specified_figsize=figsize,
                    dimension=dimension)
    return


###temporal distance plotting###

def plot_timeline(incident,
                    titles_to_ignore=None,
                    output_folder=None,
                    start_from_scratch=True,
                    language=None,
                    verbose=0):
    """extract the publication dates from an incident subcorpus and plot a timeline"""
    data_space_d = get_titles_and_publication_dates(incident=incident,
                                                    output_folder=output_folder,
                                                    titles_to_ignore=titles_to_ignore)
    hdd_l, publication_l = prepare_timeline_plot(data_space_d)

    ax1 = plt.figure(dpi=300)
    plt.plot(hdd_l, publication_l)
    plt.xlabel('N days')
    plt.ylabel('N reference texts')

    if output_folder != None:
        create_output_folder(output_folder=f"{output_folder}/output/{incident}",
                            start_from_scratch=start_from_scratch,
                            verbose=verbose)

    pdf_path = f"{output_folder}/output/{incident}/timeline.pdf"
    plt.savefig(pdf_path)
    if verbose:
        print(f"exported timeline to {pdf_path}")

###participant analysis###

def participant_info(incident,
                        selected_participants,
                        time_buckets,
                        output_folder,
                        threshold=None,
                        to_be_bundled=None,
                        language=None,
                        exclude_fes=[],
                        unexpressed=False,
                        verbose=0):
    """perform participant analysis for a given corpus, incident, time buckets and participants"""
    participant_mentions, dev = get_frequency_ranking_of_participants(output_folder, incident, verbose)
    participants_info_d = {}

    for identifier, label in selected_participants.items():
        participant_info = info_participant(identifier, time_buckets, incident, output_folder, language)
        participants_info_d[label] = participant_info

    if to_be_bundled != None:
        bundle_participants(participants_info_d, to_be_bundled, time_buckets)

    if verbose >= 2:
        extract_info(participants_info_d)

    if language == None:
        json_path = f"{output_folder}/output/{incident}/participants_info.json"
    else:
        json_path = f"{output_folder}/output/{incident}/participants_info_{language}.json"

    with open(json_path, 'w') as outfile:
        json.dump(participants_info_d, outfile, indent=4, sort_keys=True)

    if verbose:
        print(f"exported participants info to {json_path}")

    if unexpressed == True:
        anchor_unexpressed_fes_l, climax_unexpressed_fes_l, over_time_d = get_unexpressed_fes(time_buckets=time_buckets,
                                                                                                output_folder=output_folder,
                                                                                                incident=incident,
                                                                                                exclude_fes=exclude_fes)
        if verbose:
            print(f"{len(anchor_unexpressed_fes_l)+len(climax_unexpressed_fes_l)} unexpressed frame elements")

        export_unexpressed_fes(anchor_unexpressed_fes_l=anchor_unexpressed_fes_l,
                                climax_unexpressed_fes_l=climax_unexpressed_fes_l,
                                over_time_d=over_time_d,
                                output_folder=output_folder,
                                incident=incident,
                                verbose=verbose)
    return

###preprocessing###

def framing_an_incident_per_doc(project,
                                incident,
                                language,
                                event_date,
                                subevents_dict=None,
                                output_folder=None,
                                start_from_scratch=True,
                                verbose=0):
    """create a dictionary with all relevant info about the framing of a specified incident per document"""
    naf_paths = get_naf_paths(project=project,
                                incident=incident,
                                language=language,
                                verbose=verbose)
    timestamps = timestamps_collection(naf_paths[incident])
    known_timestamps, unknown_timestamps = validate_publication_date(event_date=event_date,
                                                                    timestamps=timestamps,
                                                                    verbose=verbose)
    historical_distance_list = calculate_difference(list_of_timestamps=known_timestamps,
                                                    event_date=event_date)

    titles = []
    n_entity_links = 0
    n_lus = 0
    n_fes = 0
    n_tokens = 0

    if output_folder != None:
        create_output_folder(output_folder=f"{output_folder}/output/{incident}/corpus/{language}",
                            start_from_scratch=start_from_scratch,
                            verbose=verbose)

    for path in naf_paths[incident]:
        doc_tree = etree.parse(path)
        root = doc_tree.getroot()

        if check_if_annotated(root, language) == False:
            if verbose >= 2:
                print()
                print(f"{path} has no srl layer")
                print()
            continue

        raw_text = get_raw_text(root)
        title = get_title(root)
        if verbose >= 2:
            print(title)
        titles.append(title)
        frames_dict = get_frames(root)
        frame_elements_dict = get_frame_elements(root)
        lemmas_dict = get_lemmas(root)
        remove_deprecated_mws(frames_dict, lemmas_dict, frame_elements_dict)
        entity_links_dict = get_entity_links(root, verbose)
        sentence_dict = get_sentence_info(root)
        compound_dict = get_compound_info(root, lemmas_dict, language)
        move_fes(frame_elements_dict, compound_dict)
        determiner_dict = get_determiner_info(root)
        deps_dict = deps(root)
        add_unexpressed_coresets(frames_dict, frame_elements_dict, verbose)
        check_attendee_fe(frames_dict, frame_elements_dict, verbose)

        doc_variation_dict = doc_variation(title=title,
                                            entity_links_dict=entity_links_dict,
                                            frames_dict=frames_dict,
                                            fe_dict=frame_elements_dict,
                                            lemma_dict=lemmas_dict,
                                            sentence_dict=sentence_dict,
                                            det_dict=determiner_dict,
                                            compound_dict=compound_dict,
                                            deps_dict=deps_dict,
                                            hdd_list=historical_distance_list,
                                            raw_text=raw_text,
                                            root=root)

        if subevents_dict != None:
            map_subevents_to_instance(incident=incident,
                                        language=language,
                                        subevents_dict=subevents_dict,
                                        doc_variation_dict=doc_variation_dict,
                                        verbose=verbose)

        json_path = f"{output_folder}/output/{incident}/corpus/{language}/{title}.json"
        with open(json_path, 'w') as outfile:
            json.dump(doc_variation_dict, outfile, indent=4, sort_keys=True)

        if verbose >= 2:
            print(f"exported variation dict to {json_path}")

        entity_links, lus, fes = descriptive_stats(language=language,
                                                    title=title,
                                                    incident=incident,
                                                    entity_links_dict=entity_links_dict,
                                                    frames_dict=frames_dict,
                                                    fe_dict=frame_elements_dict,
                                                    subevents_dict=subevents_dict)
        n_entity_links += len(entity_links)
        n_lus += len(lus)
        n_fes += len(fes)
        n_tokens += len(lemmas_dict)

    if verbose:
        print()
        print("descriptive statistics")
        print("number of reference texts:", len(titles))
        print("average number of tokens:", round(n_tokens/len(titles)))
        print("number of entity links:", n_entity_links)
        print("number of lexical units:", n_lus)
        #print("number of core frame elements", n_fes)

    fe_freq_l, all_fes = descriptive_fe_stats(incident=incident,
                                                language=language)

    if verbose:
        print(f"word FEs: {fe_freq_l[0][0]} ({fe_freq_l[0][1]}%)")
        print(f"sentence FEs: {fe_freq_l[1][0]} ({fe_freq_l[1][1]}%)")
        print(f"discourse FEs: {fe_freq_l[2][0]} ({fe_freq_l[2][1]}%)")
        print(f"unexpressed FEs: {fe_freq_l[3][0]} ({fe_freq_l[3][1]}%)")
        print("all core FEs: ", all_fes)
    return

def extract_hdd(project,
                incident_dict,
                output_folder=None,
                start_from_scratch=True,
                verbose=0):
    """extract historical distance in days from naf files and provide a range of data points per incident"""
    data_space_dict = {}

    for incident, info in incident_dict.items():
        for language in info["languages"]:
            data_space = []
            naf_paths = get_naf_paths(project=project,
                                        incident=incident,
                                        language=language,
                                        verbose=verbose)
            timestamps = timestamps_collection(naf_paths[incident])
            known_timestamps, unknown_timestamps = validate_publication_date(event_date=info["date"],
                                                                            timestamps=timestamps,
                                                                            verbose=verbose)
            historical_distance_list = calculate_difference(list_of_timestamps=known_timestamps,
                                                            event_date=info["date"])
            for doc in historical_distance_list:
                historical_distance = doc['historical distance']
                data_space.append(historical_distance)
            sorted_data_space = sorted(data_space)
            data_space_dict[incident][language] = sorted_data_space
    print(data_space_dict)
    return
