import json
import glob
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_clustered_stacked(dfall, colors, labels=None, figsize=None,  H="*",**kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot.
    labels is a list of the names of the dataframe, used for the legend
    title is a string for the title of the plot
    H is the hatch used for identification of the different dataframe"""
    n_df = len(dfall)
    n_col = len(dfall[0].columns)
    n_ind = len(dfall[0].index)
    #plt.style.use('tableau-colorblind10')
    fig, ax = plt.subplots(dpi=300)
    axe = plt.subplot(111)

    if figsize != None:
        for df in dfall : # for each data frame
            axe = df.plot(kind="bar",
                          figsize=figsize,
                          linewidth=0,
                          stacked=True,
                          ax=axe,
                          legend=False,
                          grid=False,
                          color=colors,
                          **kwargs)  # make bar plots
    else:
        for df in dfall : # for each data frame
            axe = df.plot(kind="bar",
                          linewidth=0,
                          stacked=True,
                          ax=axe,
                          legend=False,
                          grid=False,
                          color=colors,
                          **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)

    # Add invisible data to add another legend
    n=[]
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(
    n,
    labels,
    loc=[1.01, 0.1],
    fontsize=12,
    handleheight=1.5,
    handlelength=2,
    frameon=True,
    borderpad=1.2,
    labelspacing=1.0
)

    axe.add_artist(l1)
    plt.ylabel('proportion per TDC')
    plt.xlabel('TRD in TDCs')
    return #axe

def prepare_stacked_barplot(syntax_dict, function, ordered_tbs):
    """convert syntax dict to a data frame for plotting"""
    list_of_lists = []
    index = []
    columns = []

    for time_bucket, functions in syntax_dict.items():
        l = []
        for participant, tupl in functions[function].items():
            perc = tupl[1]
            l.append(perc)
            columns.append(participant)
        list_of_lists.append(l)
        index.append(time_bucket)
    list_of_lists = reorder_time_buckets(index, list_of_lists, ordered_tbs)
    columns = columns[:5]
    return list_of_lists, columns

def syntactic_function_distribution(participants_d):
    """create dictionary with syntactic functions per participant per time bucket"""
    syntax_dict = {} #{time_bucket: {subject: {part: N, part: N}, other: {part: N, part: N}}}

    for participant, tbs in participants_d.items():
        for tb in tbs.keys():
            syntax_dict[tb] = defaultdict(dict)

    for participant, tbs in participants_d.items():
        for tb, info in tbs.items():
            subj = 0
            other = 0
            if "syntactic function" in info.keys():
                functions = info["syntactic function"]
                for function in functions:
                    if function != None:
                        if "subj" in function:
                            subj += 1
                        else:
                            other += 1
            syntax_dict[tb]["subject"][participant] = subj
            syntax_dict[tb]["other"][participant] = other

    for tb, functions in syntax_dict.copy().items():
        for function, participants in functions.items():
            all_mentions = 0
            for participant, n in participants.items():
                all_mentions += n
            for participant, n in participants.items():
                perc = round((n*100)/all_mentions, 1)
                syntax_dict[tb][function][participant] = (n, perc)
    return syntax_dict

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
