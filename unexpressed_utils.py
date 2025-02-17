import json
import glob
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt
import pandas as pd
import statistics as s

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

def type_selection(condition, incident_d, ordered_l, output_folder, incident, verbose):
    """pre-selection of types given dimension and condition"""
    anchor_all_tokens = []
    counter_d = {}
    types_s = set()
    n_tokens_d = {}

    if condition == "anchor":
        for time_bucket, value in incident_d.items():#iterate over time_buckets:info
            n_tokens = len(value["anchor"]) #number of frames
            counter = Counter(value["anchor"]) #create count dictionary
            for token in value["anchor"]:
                anchor_all_tokens.append(token)
            n_tokens_d[time_bucket] = n_tokens #add time_bucket:N of FEs
            counter_d[time_bucket] = counter #add time_bucket:counter
        counter_anchor = Counter(anchor_all_tokens)
        most_common = counter_anchor.most_common(3)
        latex_l = []
        for tupl in most_common:
            token = tupl[0]
            freq = tupl[1]
            perc = round((freq*100)/len(anchor_all_tokens), 2)
            types_s.add(token)
            latex_l.append((token, freq, perc))
            if verbose:
                print(token, freq, perc)
        anchor_distribution_to_latex(latex_l, output_folder, incident, condition, verbose)
    else:
        for time_bucket in ordered_l:
            n_tokens = len(incident_d[time_bucket]["non-anchor"]) #number of frames
            counter = Counter(incident_d[time_bucket]["non-anchor"]) #create count dictionary
            most_common = counter.most_common(3)
            if verbose:
                print()
                print(time_bucket)
            for tupl in most_common:
                token = tupl[0]
                freq = tupl[1]
                perc = round((freq*100)/n_tokens, 2)
                types_s.add(token)
                if verbose:
                    print(token, freq, perc)
            n_tokens_d[time_bucket] = n_tokens #add time_bucket:N of FEs
            counter_d[time_bucket] = counter
    return counter_d, types_s, n_tokens_d

def restructure_unexpressed_data(incident_d, condition, ordered_l, output_folder, incident, verbose):
    """restructure particpant data for plotting"""
    plot_data = {} #{frame: {x: [day1, day2, day3], y: [percentage]}}

    counter_d, types_s, n_tokens_d = type_selection(condition, incident_d, ordered_l, output_folder, incident, verbose)

    tb_tokens_d = {} #{frame: {time_bucket: (freq, perc)}}

    for t in types_s: #iterate over types
        tdc_d = {}
        for time_bucket, counter in counter_d.items(): #iterate over time bucket:counter
            if t in counter.keys(): #if the FE type is in the counter
                type_freq = counter[t] #FE freq
                total_n = n_tokens_d[time_bucket]
                if total_n == 0:
                    type_perc = 0
                else:
                    type_perc = round((type_freq*100)/total_n) #FE percentage
                tupl = (type_freq, type_perc)
            else:
                tupl = (0, 0)
            tdc_d[time_bucket] = tupl #add time bucket: freq to dict
        tb_tokens_d[t] = tdc_d

    for fe, info in tb_tokens_d.items():
        tb_perc_d = {}
        tb_l = []
        perc_l = []
        for tb, tupl in info.items():
            tb_l.append(tb)
            perc = tupl[1]
            perc_l.append(perc)
        perc_l = reorder_time_buckets(tb_l, perc_l, ordered_l)
        tb_perc_d["tb"] = ordered_l
        tb_perc_d["perc"] = perc_l
        plot_data[fe] = tb_perc_d
    return plot_data

def anchor_distribution_to_latex(data, output_folder, incident, condition, verbose):
    """export frame distribution for the anchor incident to latex table"""
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Frame element', 'N', '%'])

    # Add row number and format 'Frame' column with fnframe
    df['Frame element'] = ['{}. \\fnframe{{{}}}'.format(i+1, x.replace('_', '\\_')) for i, x in enumerate(df['Frame element'])]

    # Generate LaTeX code for the table without caption and label, including column headers
    latex_table = df.to_latex(index=False, escape=False)

    # Manually insert the column headers
    latex_table = "\\begin{table}\n    \\centering\n    \\begin{tabular}{lcc}\n    \\toprule\n" \
                  "\\textbf{Frame element} & \\textbf{N} & \\textbf{\\%} \\\\n    \\midrule\n" + latex_table[latex_table.find('1.'):] + "\n \\end{table}"

    tex_path = f"{output_folder}/output/{incident}/tables/unexpressed/unexpressed_{condition}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")
    return
