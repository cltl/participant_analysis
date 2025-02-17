import json
import glob
import collections
from collections import defaultdict, Counter
import pprint
from itertools import islice
import matplotlib.pyplot as plt

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

def prepare_plotting(participants_d, ordered_l, dimension):
    """prepare the data for plotting"""
    plot_data = {}
    total_per_tb = defaultdict(list)

    for participant, time_buckets in participants_d.items():
        for time_bucket, info in time_buckets.items():
            if dimension in info.keys():
                for lemma in info[dimension]:
                    total_per_tb[time_bucket].append(dimension)

    for participant, time_buckets in participants_d.items():
        d = {}
        x = []
        y = []
        for time_bucket, info in time_buckets.items():
            if dimension in info.keys():
                participant_mentions = len(info[dimension])
                all_mentions = len(total_per_tb[time_bucket])
                perc = round((participant_mentions*100)/all_mentions)
            else:
                mentions = 0
                perc_mentions = 0
            x.append(time_bucket)
            y.append(perc)
        y = reorder_time_buckets(x, y, ordered_l)
        d["x"] = ordered_l
        d["y"] = y
        plot_data[participant] = d
    return plot_data

def export_plots(incident,
                plot_data,
                output_folder,
                verbose):
    """plot the reference data"""
    plt.style.use('tableau-colorblind10')

    if incident == "Q62090804":
        plt.figure(dpi=300)
        plt.plot(plot_data["victims"]["x"],plot_data["victims"]["y"], label="DpA victims")#, color="tab:blue")
        plt.plot(plot_data["Gökmen Tanis"]["x"],plot_data["Gökmen Tanis"]["y"], label="DpA Gökmen Tanis")#, color="tab:orange")
        plt.plot(plot_data["police officers"]["x"],plot_data["police officers"]["y"], label="IpA police officers", linestyle="-.")#, color="tab:green")
        plt.plot(plot_data["other suspects"]["x"],plot_data["other suspects"]["y"], label="IpA other suspects", linestyle="-.")#, color="tab:red")
        plt.plot(plot_data["Utrecht citizens"]["x"],plot_data["Utrecht citizens"]["y"], label="IpA Utrecht citizens", linestyle="-.")#, color="tab:purple")
        plt.legend(bbox_to_anchor=(1, 1))

    if incident == "Q17374096":
        plt.figure(dpi=300)
        plt.plot(plot_data["victims"]["x"],plot_data["victims"]["y"], label="DpA victims")#, color="tab:blue")
        plt.plot(plot_data["suspects"]["x"],plot_data["suspects"]["y"], label="DpA suspects")#, color="tab:orange")
        plt.plot(plot_data["relatives"]["x"],plot_data["relatives"]["y"], label="IpA relatives", linestyle="-.")#, color="tab:green")
        plt.plot(plot_data["Russian government"]["x"],plot_data["Russian government"]["y"], label="IpA Russian government", linestyle="-.")#, color="tab:red")
        plt.plot(plot_data["pro-Russian rebels"]["x"],plot_data["pro-Russian rebels"]["y"], label="IpA pro-Russian rebels", linestyle="-.")#, color="tab:purple")
        legend = plt.legend(bbox_to_anchor=(1, 1))

    if incident == "Q105077032":
        plt.figure(dpi=300)
        plt.plot(plot_data["rioters"]["x"],plot_data["rioters"]["y"], label="DpA rioters")#, color="tab:blue")
        plt.plot(plot_data["law enforcement"]["x"],plot_data["law enforcement"]["y"], label="DpA law enforcement")#, color="tab:orange")
        plt.plot(plot_data["Dutch government"]["x"],plot_data["Dutch government"]["y"], label="IpA Dutch government", linestyle="-.")#, color="tab:green")
        plt.plot(plot_data["entrepeneurs"]["x"],plot_data["entrepeneurs"]["y"], label="IpA entrepeneurs", linestyle="-.")#, color="tab:red")
        plt.plot(plot_data["citizens"]["x"],plot_data["citizens"]["y"], label="IpA citizens", linestyle="-.")#, color="tab:purple")
        legend = plt.legend(bbox_to_anchor=(1, 1))

    if incident == "Q30973589":
        plt.figure(figsize=(8,4),dpi=300)
        plt.plot(plot_data["participants"]["x"],plot_data["participants"]["y"], label="DpA participants")#, color="tab:blue")
        plt.plot(plot_data["audience"]["x"],plot_data["audience"]["y"], label="DpA audience")#, color="tab:orange")
        plt.plot(plot_data["broadcasters"]["x"],plot_data["broadcasters"]["y"], label="DpA broadcasters")#, color="tab:green")
        plt.plot(plot_data["organizers"]["x"],plot_data["organizers"]["y"], label="IpA organizers", linestyle="-.")#, color="tab:red")
        plt.plot(plot_data["European Broadcasting Union"]["x"],plot_data["European Broadcasting Union"]["y"], label="IpA EBU", linestyle="-.")#, color="tab:purple")
        plt.legend(bbox_to_anchor=(1, 1))
    plt.ylabel('proportion per TDC')
    plt.xlabel('TRD in TDCs')
    pdf_path = f"{output_folder}/output/{incident}/figures/interfaces/discourse_distribution.pdf"
    plt.savefig(pdf_path, bbox_inches='tight')
    if verbose:
        print(f"exported plot to {pdf_path}")
