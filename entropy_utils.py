import json
import glob
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt
import pandas as pd
import pprint
import numpy as np
from scipy.stats import entropy
from math import log, e
import scipy

def normalized_entropy(tokens, base):
    """calculate normalized entropy (range 0-1)"""
    counts = Counter(tokens)  # Get token frequencies
    probs = np.array(list(counts.values())) / len(tokens)  # Convert to probabilities
    H = entropy(probs, base=base)  # Compute entropy
    H_max = np.log(len(counts)) / np.log(base)  # Compute max entropy
    return round(H / H_max if H_max > 0 else 0, 2)  # Normalize

def calculate_entropy(d, feature, ordered_tbs, base=2):
    """calculate entropy per incident per mention type"""
    ent_d = defaultdict(list)
    for participant in d:
        for tdc in ordered_tbs:
            if feature in d[participant][tdc].keys():
                entropy_value = normalized_entropy(d[participant][tdc][feature], base)
            else:
                entropy_value = 0
            ent_d[participant].append((tdc, entropy_value))
    return ent_d

def calculate_unexpressed_entropy(d, ordered_tbs, base=2):
    """calculate entropy per incident per mention type"""
    ent_d = {}
    ent_anchor_l = []
    ent_climax_l = []
    for tdc in ordered_tbs:
        entropy_value = normalized_entropy(d[tdc]["anchor"], base)
        ent_anchor_l.append((tdc, entropy_value))
        entropy_value = normalized_entropy(d[tdc]["non-anchor"], base)
        ent_climax_l.append((tdc, entropy_value))
    ent_d["anchor"] = ent_anchor_l
    ent_d["climax"] = ent_climax_l
    return ent_d

def entropy_to_latex(frames_entropy_d, feature, output_folder, verbose):
    # Convert dictionary to DataFrame-friendly format
    latex_str = r"""\begin{table}[!ht]
    \begin{center}
    \begin{tabular}{lcc}
        \hline
    """

    for event, values in frames_entropy_d.items():
        # Add event title as a multicolumn row
        latex_str += f"    \\multicolumn{{3}}{{c}}{{\\textbf{{{event}}}}} \\\\\n"
        latex_str += "      \\hline\n"
        latex_str += "      \\textbf{temporal distance class} & \\textbf{anchor} & \\textbf{climax} \\\\\n"
        latex_str += "      \\hline\n"

        # Loop through data and format rows correctly
        for i, ((time, anchor), (_, climax)) in enumerate(zip(values['anchor'], values['climax']), start=1):
            #time_formatted = time.replace("--", " to ").replace("-", " to ")  # Format negative ranges

            latex_str += f"      {i}. Day {time} & {anchor:.2f} & {climax:.2f} \\\\\n"
        latex_str += "      \\hline\n"

    # Close table
    latex_str += r"""
    \end{tabular}
    \end{center}
    \end{table}"""

    tex_path = f"{output_folder}/output/entropy_{feature}.tex"

    with open(tex_path, "w") as f:
        f.write(latex_str)
        if verbose:
            print(f"exported table to {tex_path}")
