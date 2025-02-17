from .DFNDataReleases import get_relevant_info
from .DFNDataReleases import dir_path as REPO_DIR
from collections import defaultdict
import os
import json
import pprint

def get_naf_paths(project, incident,language,verbose=0):
    """
    Get a dictionary with incident identifier as key and a set of NAF paths as value.
    :param project: the project under which the NAF files are generated.
    :param language: the language of the reference texts.
    :type project: string
    :type language: string
    """
    relevant_info = get_relevant_info(repo_dir=REPO_DIR,
                                    project=project,
                                    load_jsons=True)
    incident_collection = defaultdict(set)

    if language in relevant_info['inc2lang2doc'][incident]:
        doc_list = relevant_info['inc2lang2doc'][incident][language]
        for doc in doc_list:
            path = os.path.join(relevant_info["unstructured"], language, f"{doc}.naf")
            assert os.path.exists(path), f"{path} does not exist on disk"
            incident_collection[incident].add(path)

    if verbose >= 2:
        print(f'{incident}: {len(incident_collection[incident])} reference texts in {language}')
    return incident_collection
