import json
import glob
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt
import pandas as pd
import statistics as s
import numpy as np

def compounds_to_latex(df, output_folder, verbose):
    latex_table = df.to_latex()
    tex_path = f"{output_folder}/output/compound_distribution.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")

def compound_analysis(compounds_d):
    """conduct compound analysis"""
    ipa_l = compounds_d["indirect participants"]
    new_ipa_l = remove_values_from_list(ipa_l, "mh17-verdachte")
    new_ipa_l = remove_values_from_list(new_ipa_l, "mh17-verdachen")
    new_ipa_l = remove_values_from_list(new_ipa_l, "cockpitbemanning")
    new_ipa_l = remove_values_from_list(new_ipa_l, "tramschutter")
    new_ipa_l = remove_values_from_list(new_ipa_l, "songfestivalfan")
    new_ipa_l = remove_values_from_list(new_ipa_l, "onderzoeksraad")
    compounds_d.update({"indirect participants": new_ipa_l})

    for x in range(9):
        compounds_d["direct participants"].append("mh17-verdachte")
    for x in range(2):
        compounds_d["direct participants"].append("cockpitbemanning")
        compounds_d["direct participants"].append("songfestivalfan")

    compounds_d["direct participants"].append("tramschutter")
    n_dpas = len(compounds_d["direct participants"])
    n_ipas = len(compounds_d["indirect participants"])
    total = n_dpas+n_ipas
    perc_dpas = round((n_dpas*100)/total, 2)
    perc_ipas = round((n_ipas*100)/total, 2)
    print(f"relative frequency of compounds referring to directly related participants: {perc_dpas}%")
    print(f"relative frequency of compounds referring to indirectly related participants: {perc_ipas}%")
    dpa_distribution = distribution(compounds_d["direct participants"], 10)
    df1 = pd.DataFrame(columns=["compound", "freq", "%"], data=dpa_distribution)
    ipa_distribution = distribution(compounds_d["indirect participants"], 10)
    df2 = pd.DataFrame(columns=["compound", "freq", "%"], data=ipa_distribution)
    concatenated_df = pd.concat([df1, df2], axis=1)
    return concatenated_df

def distribution(compound_l, ranking):
    """get a frequency distribution of unexpressed frame elements"""
    distribution = []
    count = Counter(compound_l)
    most_common = count.most_common(ranking)
    for tupl in most_common:
            compound = tupl[0]
            freq = tupl[1]
            perc = round((freq*100)/len(compound_l), 1)
            compound_freq_perc = (compound, freq, perc)
            distribution.append(compound_freq_perc)
    return distribution

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def head_distribution_to_latex(ds, incident, output_folder, participant, language, verbose):
    table = pd.concat(ds, axis=0)
    latex_table = table.to_latex()
    tex_path = f"{output_folder}/output/{incident}/tables/lexical units/head_distribution_{participant}_{language}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")

def top_ranked_lus(participant_d):
    """rank top frequent lus with absolute and relative frequency"""
    ds = []
    d = {}

    for tb, info in participant_d.items():
        tb_d = {}
        count = 0
        if "reftype:evokes" in info.keys():
            evokes_l = info["reftype:evokes"]
            counter = Counter(evokes_l) #create count dictionary
            most_common = counter.most_common(5)
            lu_l = []
            freq_l = []
            perc_l = []
            for tupl in most_common:
                lu = tupl[0]
                freq = tupl[1]
                perc = round((freq*100)/len(evokes_l), 1)
                count += 1
                lu_l.append(lu)
                freq_l.append(freq)
                perc_l.append(perc)
            tb_d["lexical unit"] = lu_l
            tb_d["N"] = freq_l
            tb_d["%"] = perc_l
            df = pd.DataFrame(data=tb_d)
            d[tb] = df

    ds.append(pd.concat(d, axis=1))
    return ds

def evokes_distribution_to_latex(ds, incident, language, output_folder, verbose):
    concat_ds = pd.concat(ds, axis=0)
    latex_table = concat_ds.to_latex()
    tex_path = f"{output_folder}/output/{incident}/tables/lexical units/types-tokens_{language}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")

def evokes_distribution(participants_d):
    """show distribution of types and tokens per participant and per time bucket"""
    ds = []

    for participant, time_buckets in participants_d.items():
        d = {}
        for time_bucket, info in time_buckets.items():
            if "reftype:evokes" in info.keys():
                evokes_l = info["reftype:evokes"]
                tokens = len(evokes_l)
                types = len(set(evokes_l))
                ratio = round(types/tokens, 2)
            else:
                tokens = 0
                types = 0
                ratio = 0
            d[time_bucket] = pd.DataFrame(columns=['participant', 'tokens', 'types', 'ratio'],
                                         data=[[participant, tokens, types, ratio]]).set_index('participant')
        ds.append(pd.concat(d, axis=1))
    return ds

def extract_pos_info(participants_d, participant, ordered_tbs):
    """prepare participant POS data for plotting"""
    tbs_l = []
    plot_data = defaultdict(list)

    for time_bucket, info in participants_d[participant].items():
        noun = []
        propn = []
        if "POS" in info.keys():
            for token in info["POS"]:
                if token == "NOUN":
                    noun.append(token)
                elif token == "PROPN":
                    propn.append(token)
                else:
                    continue
        total = len(noun+propn)
        if total == 0:
            perc_noun = 0
            perc_propn = 0
        else:
            perc_noun = round((len(noun)*100)/total)
            perc_propn = round((len(propn)*100)/total)
        tbs_l.append(time_bucket)
        plot_data["NOUN"].append(perc_noun)
        plot_data["PROPN"].append(perc_propn)

    perc_noun_l = reorder_time_buckets(tbs_l, plot_data["NOUN"], ordered_tbs)
    perc_propn_l = reorder_time_buckets(tbs_l, plot_data["PROPN"], ordered_tbs)

    plot_data["NOUN"] = np.array(perc_noun_l)
    plot_data["PROPN"] = np.array(perc_propn_l)
    return plot_data

def reorder_time_buckets(unordered_tbs, unordered_perc, ordered_tbs):
    "reorder time buckets for plotting"
    tbs_perc = []

    for x, y in zip(unordered_tbs, unordered_perc):
        tbs_perc.append((x,y))

    ordered_perc = []

    for tdc in ordered_tbs:
        for tupl in tbs_perc:
            if tupl[0] == tdc:
                ordered_perc.append(tupl[1])
    return ordered_perc

def plot_pos(plot_data, n_columns, ordered_l, output_folder, incident, participant, verbose):
    """plot the POS relative frequency distribution"""
    width = 0.5
    plt.style.use('tableau-colorblind10')
    fig, ax = plt.subplots(dpi=300)
    bottom = np.zeros(n_columns)

    for pos, percentages in plot_data.items():
        p = ax.bar(ordered_l, percentages, width, label=pos, bottom=bottom)
        bottom += percentages

    plt.ylabel('proportion per TDC')
    plt.xlabel('TRD in TDCs')
    legend = ax.legend(bbox_to_anchor=(1, 1))
    pdf_path = f"{output_folder}/output/{incident}/figures/lexical units/pos_{participant}.pdf"

    plt.savefig(pdf_path, bbox_inches='tight')
    if verbose:
        print(f"exported barplot to {pdf_path}")
