import urllib.request as urllib


def download(url, files):
    for f in files:
        urllib.urlretrieve(url + f, f)


# DBpedia
url = "https://raw.githubusercontent.com/smart-task/smart-dataset/master/datasets/DBpedia/"
files = [
    "smarttask_dbpedia_test.json",
    "smarttask_dbpedia_test_questions.json",
    "smarttask_dbpedia_train.json"
]

download(url, files)

# Wikidata
url = "https://raw.githubusercontent.com/smart-task/smart-dataset/master/datasets/Wikidata/"
files = [
    "lcquad2_anstype_wikidata_test.json",
    "lcquad2_anstype_wikidata_test_gold.json ",
    "lcquad2_anstype_wikidata_train.json",
    "wikidata__qid_label.csv"
]

download(url, files)
