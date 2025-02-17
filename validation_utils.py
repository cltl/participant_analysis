import pickle

def map_subevents_to_instance(incident, language, subevents_dict, doc_variation_dict, verbose):
    """categorize predicates referencing the main event under its instance in doc_variation_dict"""
    linked_predicates = []

    for title, categories in doc_variation_dict.items():
        if "subevents" in categories.keys():
            for term, info in categories["subevents"].copy().items():
                for predicate in subevents_dict[incident][language][title]:
                    target = predicate[0]
                    lemma = predicate[1]
                    if term == target:
                        if "frames/links" not in categories.keys():
                            categories["frames/links"] = {incident: {term: info}}
                        elif incident not in categories["frames/links"]:
                            categories["frames/links"][incident] = {term: info}
                        else:
                            categories["frames/links"][incident][term] = info
                        del categories["subevents"][term]
                        linked_predicates.append(lemma)

    if verbose >= 3 and len(linked_predicates) > 0:
        print(title)
        print(f"linked {', '.join(linked_predicates)} to {incident}")
        print()
    return
