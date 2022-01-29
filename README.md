# Overview
Basic ontology class predictor for [ISWC 2020 SMART Task](https://smart-task.github.io/2020/).

Currently only uses [Wikidata training dataset](https://raw.githubusercontent.com/michal-kapala/smart-prediction-task-iswc2020/master/Wikidata/lcquad2_anstype_wikidata_train.json) to select answer candidates for `resource` type of questions. The returned Q-items are types of those entities which have any of the nouns included in a question as part of their descriptions in [labels set](https://github.com/michal-kapala/smart-prediction-task-iswc2020/blob/master/Wikidata/wikidata__qid_label.csv).

# Scripts

- [`download.py`](https://github.com/michal-kapala/smart-prediction-task-iswc2020/blob/master/download.py) - downloads dataset and label files
- [`helper.py`](https://github.com/michal-kapala/smart-prediction-task-iswc2020/blob/master/helper.py) - functions for file management, convertions and text processing
- [`main.py`](https://github.com/michal-kapala/smart-prediction-task-iswc2020/blob/master/main.py) - main flow for the predictor
- [`queries.py`](https://github.com/michal-kapala/smart-prediction-task-iswc2020/blob/master/queries.py) - parameterized SPARQL queries
