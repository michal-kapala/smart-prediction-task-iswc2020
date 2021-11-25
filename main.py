import os
import json
import pandas as pd

# loads a JSON dataset
def load_dataset(filename):
    is_dbpedia = True if (filename.find("dbpedia") >= 0) else False
    root_dir = os.path.dirname(__file__)
    sub_folder = "DBpedia" if is_dbpedia else "Wikidata"
    dir = os.path.join(root_dir + f"\\{sub_folder}")
    dir = os.path.join(dir, filename)
    file = open(dir)
    return json.load(file)

# loads ontology classes list as pd.DataFrame
def load_wikidata_categories():
    root_dir = os.path.dirname(__file__)
    dir = os.path.join(root_dir + "\\Wikidata\\wikidata__qid_label.csv")
    file = open(dir, encoding="utf8")
    return pd.read_csv(file, delimiter="|")

# print(load_dataset("lcquad2_anstype_wikidata_train.json"))
# print(load_wikidata_categories())