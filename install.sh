#!/usr/bin/env bash

rm -f classes.py
wget https://raw.githubusercontent.com/cltl/multilingual-wiki-event-pipeline/master/classes.py
wget https://raw.githubusercontent.com/cltl/SpaCy-to-NAF/master/spacy_to_naf.py

rm -rf resources
mkdir resources
cd resources

git clone https://github.com/cltl/FN_Reader
cd FN_Reader
pip install -r requirements.txt
bash install.sh
cd ..