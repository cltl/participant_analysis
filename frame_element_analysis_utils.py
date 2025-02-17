import json
import glob
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt
import pandas as pd
import statistics as s

def plot_lu_offset(x, y, ordered_l, output_folder, incident, dimension, condition, language, specified_figsize, verbose):
    """prepare the data for plotting"""
    plot_data = {}
    y = reorder_time_buckets(x, y, ordered_l)
    plot_data["x"] = ordered_l
    plot_data["y"] = y

    if specified_figsize != None:
        plt.figure(figsize=specified_figsize, dpi=300)
    else:
        plt.figure(dpi=300)

    plt.ylabel('average LU-frame offset per TDC')
    plt.xlabel('TRD in TDCs')
    plt.plot(plot_data["x"],plot_data["y"])
    pdf_path = f"{output_folder}/output/{incident}/figures/{dimension}/{dimension}_LU-frame-offset_{condition}_{language}.pdf"
    plt.savefig(pdf_path, bbox_inches='tight')
    if verbose:
        print(f"exported plot to {pdf_path}")
    return

def lu_distribution(incident_d, ordered_l=None):
    """show distribution of frame types and tokens per time bucket"""
    distribution_d = defaultdict(set)

    for tb, value in incident_d["anchor"].items(): #iterate over all frames
        for tupl in value["joint"]:
            frame = tupl[0]
            lu = tupl[1]
            distribution_d[frame].add(lu) #add all lu types per frame to dict

    avg_ratios = []
    tbs = []

    for tb, value in incident_d["anchor"].items(): #iterate over time buckets of anchor frames
        tb_d = defaultdict(set) #dict for time bucket
        for tupl in value["joint"]:
            frame = tupl[0]
            lu = tupl[1]
            tb_d[frame].add(lu) #add all lu types per frame to dict
        ratios_l = []
        for frame, lus in tb_d.items(): #iterate over frames
            n_lus = len(lus) #number of anchor lu types
            total_n_lus = len(distribution_d[frame]) #number of all lu types
            ratio = n_lus/total_n_lus #ratio
            ratios_l.append(ratio) #append ratio to list
        average = round(s.mean(ratios_l), 2) #average ratio of lexical variation within a frame for time bucket
        avg_ratios.append(average) #append average ratio to list
        tbs.append(tb)

    d = {'TDC': tbs, 'avg ratio': avg_ratios}
    return d

def remove_named_events(data_d):
    """remove all named event tokens from the data space"""
    for condition, tbs in data_d.copy().items():
        for tb, value in tbs.items():
            updated_frames_l = list(filter(lambda a: a != "MH17", value["frames"]))
            value["frames"] = updated_frames_l
            updated_lu_l = list(filter(lambda a: a != "mh17", value["lexical units"]))
            value["lexical units"] = updated_lu_l
            updated_frames_l2 = list(filter(lambda a: a != "Eurovision", value["frames"]))
            value["frames"] = updated_frames_l2
            updated_lu_l2 = list(filter(lambda a: a != "eurovision.propn", value["lexical units"]))
            value["lexical units"] = updated_lu_l2
            updated_lu_l3 = list(filter(lambda a: a != "esc.propn", value["lexical units"]))
            value["lexical units"] = updated_lu_l3
    return

def frames_distribution(incident_d, output_folder, incident, verbose, ordered_l=None):
    """show distribution of frame types and tokens per time bucket"""
    ds = []

    for condition, time_buckets in incident_d.items():
        d = {}
        for tb, info in time_buckets.items():
            frames_l = info["frames"]
            tokens = len(frames_l)
            types = len(set(frames_l))
            ratio = round(types/tokens, 2)
            d[tb] = pd.DataFrame(columns=['condition', 'types', 'tokens', 'ratio'],
                                    data=[[condition, types, tokens, ratio]]).set_index('condition')
        if ordered_l != None:
            ds.append(pd.concat(d, axis=1)[ordered_l])
        else:
            ds.append(pd.concat(d, axis=1))

    df = pd.concat(ds, axis=0)
    latex_table = df.to_latex(multicolumn=True, multirow=True)
    tex_path = f"{output_folder}/output/{incident}/tables/frames/frames_types-tokens.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")
    return

def plot_figure(plot_data, output_folder, participant, incident, verbose, specified_figsize, dimension, interfaces=False, unexpressed_condition=None):
    """plot a figure"""
    if specified_figsize != None:
        plt.figure(figsize=specified_figsize, dpi=300)
    else:
        plt.figure(dpi=300)

    plt.style.use('tableau-colorblind10')

    for label, data in plot_data.copy().items():
        plt.plot(plot_data[label]["tb"], plot_data[label]["perc"], label=label)

    plt.ylabel('proportion per TDC')
    plt.xlabel('TRD in TDCs')
    legend = plt.legend(bbox_to_anchor=(1,1))

    if interfaces == True:
        if dimension == "unexpressed":
            pdf_path = f"{output_folder}/output/{incident}/figures/interfaces/{dimension}_{unexpressed_condition}.pdf"
        else:
            pdf_path = f"{output_folder}/output/{incident}/figures/interfaces/{dimension}_{participant}.pdf"
    else:
        pdf_path = f"{output_folder}/output/{incident}/figures/{dimension}/{dimension}_{participant}.pdf"

    plt.savefig(pdf_path, bbox_inches='tight')
    if verbose:
        print(f"exported plot to {pdf_path}")
    return

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

def type_selection(participant, dimension, participants_d, verbose):
    """pre-selection of types given dimension and condition"""
   # all_tokens = []
    counter_d = {}
    types_s = set()
    n_tokens_d = {}
   # coverage_l = []

    for time_bucket, info in participants_d[participant].items(): #iterate over time_buckets:info
        #tb_d = {}
        if dimension in info.keys(): #check if frames are present
            n_tokens = len(info[dimension]) #number of frames
            counter = Counter(info[dimension]) #create count dictionary
            most_common = counter.most_common(3)
            if verbose:
                print()
                print(time_bucket)
            for tupl in most_common:
                token = tupl[0]
                freq = tupl[1]
                perc = round((freq*100)/n_tokens, 2)
                types_s.add(token)
               # tb_d[token] = {"N": freq, "%": perc}
                if verbose:
                    print(token, freq, perc)
        else:
            n_tokens = 0
            type_selection = set()
            counter = {}
       # tb_d2 = {time_bucket: tb_d}
       # coverage_l.append(sorted_dict)
        n_tokens_d[time_bucket] = n_tokens #add time_bucket:N of FEs
        counter_d[time_bucket] = counter

    #pprint.pprint(coverage_l)
    return counter_d, types_s, n_tokens_d

def restructure_data(participants_d, participant, ordered_l, dimension, verbose): #, output_folder, incident, language, verbose):
    """restructure particpant data for plotting"""
    plot_data = {} #{frame: {x: [day1, day2, day3], y: [percentage]}}

    counter_d, types_s, n_tokens_d = type_selection(participant, dimension, participants_d, verbose) # output_folder, incident, ordered_l, language, verbose)

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
    df = pd.DataFrame(data, columns=['Frame', 'N', '%'])

    # Add row number and format 'Frame' column with fnframe
    df['Frame'] = ['{}. \\fnframe{{{}}}'.format(i+1, x.replace('_', '\\_')) for i, x in enumerate(df['Frame'])]

    # Generate LaTeX code for the table without caption and label, including column headers
    latex_table = df.to_latex(index=False, escape=False)

    # Manually insert the column headers
    latex_table = "\\begin{table}\n    \\centering\n    \\begin{tabular}{lcc}\n    \\toprule\n" \
                  "\\textbf{Frame} & \\textbf{N} & \\textbf{\\%} \\\n    \\midrule\n" + latex_table[latex_table.find('1.'):] + "\n \\end{table}"

    tex_path = f"{output_folder}/output/{incident}/tables/frames/frames_{condition}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")
    return

def anchor_lus_distribution_to_latex(data, output_folder, incident, condition, language, verbose):
    """export frame distribution for the anchor incident to latex table"""
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['LU', 'N', '%'])

    # Add row number and format 'Frame' column with fnframe
    df['LU'] = ['{}. {}'.format(i+1, x.replace('_', '\\_')) for i, x in enumerate(df['LU'])]

    # Generate LaTeX code for the table without caption and label, including column headers
    latex_table = df.to_latex(index=False, escape=False)

    # Manually insert the column headers
    latex_table = "\\begin{table}\n    \\centering\n    \\begin{tabular}{lcc}\n    \\toprule\n" \
                  "\\textbf{LU} & \\textbf{N} & \\textbf{\\%} \\\n    \\midrule\n" + latex_table[latex_table.find('1.'):] + "\n \\end{table}"

    tex_path = f"{output_folder}/output/{incident}/tables/lexical units/lexical_units_{condition}_{language}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_table)
        if verbose:
            print(f"exported table to {tex_path}")
    return
