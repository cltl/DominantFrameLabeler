"""
Dominant Frame Labeler

Usage:
  dominant_frame_labeler.py --bin_folder=<bin_folder> --naf_folder=<naf_folder> \
  --output_folder=<output_folder> --pos2fn_pos=<pos2fn_pos> \
  --tf_idf_minimum_threshold=<tf_idf_minimum_threshold> \
  --verbose=<verbose>

Options:
    --bin_folder=<bin_folder> folder with *bin files containing stored classes.IncidentCollection files
    --naf_folder=<naf_folder> folder with *naf files containing the srl layer
    --output_folder=<output_folder> where the output will be stored
    --pos2fn_pos=<pos2fn_pos> only use expressions with these FrameNet parts of speech, e.g, 'NOUN-N;VERB-V;ADJ-A'
    --tf_idf_minimum_threshold=<tf_idf_minimum_threshold> any expression or more with antf-idf value above this threshold will be used
    --verbose=<verbose> 0 nothing, 1 descriptive stats, 2 debugging information

Example:
    python dominant_frame_labeler.py --bin_folder="../multilingual-wiki-event-pipeline/bin/" \
    --naf_folder="../multilingual-wiki-event-pipeline/pilot_data/naf_srl/NAF" \
    --output_folder="output" --pos2fn_pos="NOUN-N;VERB-V;ADJ-A" --tf_idf_minimum_threshold=0.8 --verbose=2
"""
from docopt import docopt
from pathlib import Path
from shutil import rmtree

import xml_utils
import tf_idf_utils

# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS')
print(arguments)
print()

# parse arguments
output_folder = Path(arguments['--output_folder'])
if output_folder.exists():
    rmtree(str(output_folder))
output_folder.mkdir()

verbose = int(arguments['--verbose'])
tf_idf_threshold = float(arguments['--tf_idf_minimum_threshold'])
pos_mapping = {}
for pos2fn_pos in arguments['--pos2fn_pos'].split(';'):
    pos, fn_pos = pos2fn_pos.split('-')
    pos_mapping[pos] = fn_pos

# load data
event_type2naf_paths = xml_utils.get_eventtype2naf_paths(bin_folder=arguments['--bin_folder'],
                                                         naf_folder=arguments['--naf_folder'],
                                                         language='en',
                                                         verbose=verbose)

event_type2info = {}
for event_type, naf_paths in event_type2naf_paths.items():
    frame2freq = xml_utils.get_label2freq(naf_paths,
                                          xpath_query='srl/predicate',
                                          attributes=['uri'],
                                          verbose=verbose)

    lemma_pos2freq = xml_utils.get_label2freq(naf_paths,
                                              xpath_query='terms/term',
                                              attributes=['lemma', 'pos'],
                                              pos_mapping=pos_mapping, # mapping pos to FrameNet part of speech
                                              verbose=verbose)

    # TODO: this should probably be a class object instead of a dictionary
    event_type2info[event_type] = {
        'frame2freq': frame2freq,
        'lemma_pos2freq': lemma_pos2freq,
        'lemma_pos_corpus': ' '.join(tf_idf_utils.dict2list_of_all_occurrences(lemma_pos2freq)),
        'frame_corpus': ' '.join(tf_idf_utils.dict2list_of_all_occurrences(frame2freq)),
    }

# perform tf idf
to_analyze = ['lemma_pos_corpus',
              'frame_corpus']
for nlp_task in to_analyze:
    print()
    print(f'performing tf-idf for {nlp_task}')

    eventtype2corpus = {
        eventtype : info[nlp_task]
        for eventtype, info in event_type2info.items()
    }

    corpus2label2tfidf_value = tf_idf_utils.compute_tfidf(eventtype2corpus,
                                                          verbose=verbose)







