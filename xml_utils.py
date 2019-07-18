import os
import pickle
from glob import glob
from collections import defaultdict
from lxml import etree


def get_eventtype2naf_paths(bin_folder,
                            naf_folder,
                            language,
                            verbose=0):
    eventtype2naf_paths = defaultdict(set)
    for bin_file in glob(f'{bin_folder}/*bin'):
        incident_collection = pickle.load(open(bin_file, 'rb'))
        eventtype = incident_collection.incident_type

        for incident in incident_collection.incidents:
            for ref_text_obj in incident.reference_texts:
                if ref_text_obj.language == language:
                    naf_path = os.path.join(naf_folder, f'{ref_text_obj.name}.naf')
                    assert os.path.exists(naf_folder), f'{naf_path} does not seem to exist on disk'
                    eventtype2naf_paths[eventtype].add(naf_path)

    if verbose >= 1:
        print()
        for event_type, naf_paths in eventtype2naf_paths.items():
            print(f'found {len(naf_paths)} NAF paths for {event_type} in language {language}')
    return eventtype2naf_paths


def get_label2freq(naf_paths, xpath_query, attributes, pos_mapping={}, verbose=0):
    """

    :param naf_paths:
    :param xpath_query:
    :param attributes:
    :param dict mapping: if a pos_mapping is provided, only those
    terms with the pos included in the pos_mapping will be used and mapped
    :param verbose:
    :return:
    """
    pos_tagset = set()

    label2freq = defaultdict(int)
    for naf_path in naf_paths:
        doc = etree.parse(naf_path)
        for el in doc.xpath(xpath_query):

            values = []
            to_add = True

            for attribute in attributes:
                value = el.get(attribute)

                if attribute == 'pos':
                    pos_tagset.add(value)
                    if pos_mapping:
                        if value in pos_mapping:
                            value = pos_mapping[value]
                        else:
                            # this means that the pos is not in the chosen set
                            to_add = False
                            continue

                values.append(value)

            if to_add:
                value_string = '---'.join(values)
                label2freq[value_string] += 1

    if verbose >= 1:
        print()
        print(f'ran function with {xpath_query} {attributes}')
        print(f'pos tags found: {pos_tagset}')
        print(f'found {sum(label2freq.values())} occurrences of {len(label2freq)} unique labels')

    return label2freq
