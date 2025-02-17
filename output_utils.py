import os
import shutil
import json
import glob
import pandas as pd

def create_output_folder(output_folder, start_from_scratch, verbose):
    '''creates output folder for export dataframe'''
    if os.path.isdir(output_folder):
        if start_from_scratch == True:
            shutil.rmtree(output_folder)
            if verbose >= 1:
                print(f"removed existing folder {output_folder}")

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        if verbose >= 1:
            print(f"created folder at {output_folder}")

def variation_to_excel(output_folder, verbose):
    """export linguistic framing information for all documents to excel"""
    headers = ["title",
          "target",
          "referent",
          "frame",
          "reftype",
          "frame elements",
          "POS",
          "lemma",
          "target phrase",
          "sentence",
          "article definite",
          "compound",
          "function",
          "historical distance"]

    list_of_lists = []

    for filename in glob.glob(f"{output_folder}/*"):
        print(filename)
        with open(filename, 'r') as infile:
            json_dict = json.load(infile)

        for title, infotype in json_dict.items():
            hd = infotype["historical distance"]
            for wiki_id, targets in infotype["frames/links"].items():
                for target, info_d in targets.items():
                    frame = info_d["frame"]
                    if "reftype" in info_d:
                        reftype = info_d["reftype"]
                    else:
                        reftype = ""
                    fes = info_d["frame elements"]
                 #   if fes != None:
                 #       fes = ', '.join(fes)
                    pos = info_d["POS"]
                    lemma = info_d["lemma"]
                    if "target phrase" in info_d:
                        phrase = info_d["target phrase"]
                    else:
                        phrase = ""
                    if "sentence" in info_d:
                        sentence = int(info_d["sentence"])
                    else:
                        sentence = ""
                    article_def = info_d["article"]["definite"]
                    if "compound" in info_d:
                        compound = info_d["compound"]
                        function = info_d["function"]
                    else:
                        compound = ""
                        function = ""
                    if fes != None:
                #        fes = ', '.join(fes)
                        for fe in fes:
                            one_row = [title, target, wiki_id, frame, reftype, fe, pos, lemma, phrase, sentence, article_def, compound, function, hd]
                            list_of_lists.append(one_row)
                    else:
                        one_row = [title, target, wiki_id, frame, reftype, "", pos, lemma, phrase, sentence, article_def, compound, function, hd]
                        list_of_lists.append(one_row)
            for target, info_d in infotype["subevents"].items():
                if "POS" not in info_d:
                    continue
                else:
                    frame = info_d["frame"]
                    if "reftype" in info_d:
                        reftype = info_d["reftype"]
                    else:
                        reftype = ""
                    fes = info_d["frame elements"]
                   # if fes != None:
                   #     fes = ', '.join(fes)
                    pos = info_d["POS"]
                    lemma = info_d["lemma"]
                    if "target phrase" in info_d:
                        phrase = info_d["target phrase"]
                    else:
                        phrase = ""
                    if "sentence" in info_d:
                        sentence = int(info_d["sentence"])
                    else:
                        sentence = ""
                    article_def = info_d["article"]["definite"]
                    if "compound" in info_d:
                        compound = info_d["compound"]
                        function = info_d["function"]
                    else:
                        compound = ""
                        function = ""
                    if fes != None:
                        for fe in fes:
                            one_row = [title, target, "", frame, reftype, fe, pos, lemma, phrase, sentence, article_def, compound, function, hd]
                            list_of_lists.append(one_row)
                    else:
                        one_row = [title, target, "", frame, reftype, "", pos, lemma, phrase, sentence, article_def, compound, function, hd]
                        list_of_lists.append(one_row)
            implicated = infotype["implicated fe's"]
            for fe in implicated:
                one_row = [title, "implicated", "", "", "", fe, "", "", "", "", "", "", "", hd]
                list_of_lists.append(one_row)

    df = pd.DataFrame(list_of_lists, columns=headers)
    df.to_excel(f"{output_folder}/annotations_per_doc.xlsx", index=False)

    if verbose:
        print("framing information exported to excel")
