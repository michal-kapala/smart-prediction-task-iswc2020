import numpy as np
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from helper import *

# Config
dataset_file = "lcquad2_anstype_wikidata_train.json"
is_dbpedia = True if (dataset_file.find("dbpedia") >= 0) else False
sparql_endpoint = "https://query.wikidata.org/sparql" if is_dbpedia == False else  "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(sparql_endpoint)

# ETL
dataset_wd = load_dataset(dataset_file, is_dbpedia)
categories_wd = load_wikidata_categories()                      # Numery i nazwy kategorii

dataset_wd_df = prepare_dataset_wd(pd.DataFrame(dataset_wd))    # id pytania / pytanie / kategoria / typy
dataset_wd_df_empty = dataset_wd_df.iloc[0:0]                   # same nagłówki
tokenized_wd_df = tokenize(dataset_wd_df.head(5))                       # id pytania / ztokenizowane pytanie

# print(tokenized_wd_df)

# Query for 'instance-of' of myid
myid = "wd:Q7889"

sparql.setQuery(
    '''
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    ''' +
    'SELECT DISTINCT ?item ?itemLabel WHERE { ?item wdt:P31 ' +
    f'{myid}. ' +
    'SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } } LIMIT 10'
)
sparql.setReturnFormat(JSON)
qresult = sparql.query().convert()

# DataFrame conversion
df_qresult = sparql2df(qresult)
print(df_qresult)


#for res in qresult['results']['bindings']:
    #print(res)
    # print('Type: ' + res['itemLabel']['type'] + '\tValue: ' + res['itemLabel']['value'])

# tokenized_wd_df_empty = tokenized_wd_df.iloc[0:0]               # same nagłówki
# dataset_wd_df = dataset_wd_df.drop(columns=["question"])        # dataset_wd_df bez pytania
# 
# X = dataset_wd_df.head(1000).drop(['id', 'category_x'], axis=1).to_numpy()
# y = tokenized_wd_df.head(1000).to_numpy()
# 
# clf = RandomForestClassifier(max_depth=2, n_estimators=20, verbose=2)
# clf.fit(X, y)
# 
# #Testowy dataset
# test_wd = load_dataset("lcquad2_anstype_wikidata_test_gold.json")
# 
# test_wd_df = prepare_dataset_wd(pd.DataFrame(test_wd)).head(1000)
# test_wd_df = dataset_wd_df_empty.append(test_wd_df, sort=False)
# token_test_wd_df = tokenize(test_wd_df).head(1000)
# token_test_wd_df = tokenized_wd_df_empty.append(token_test_wd_df, sort=False).fillna(0)
# test_wd_df = test_wd_df.drop(columns=["question"]).fillna(0)
# 
# Xt = test_wd_df.drop(['id', 'category'], axis=1).to_numpy()
# yt = token_test_wd_df.to_numpy()
# Xt = Xt[:, :X.shape[1]]
# yt = yt[:, :y.shape[1]]
# 
# prediction = clf.predict(Xt)
#
#rounded_prediction = np.argmax(prediction, axis=1)
#rounded_test = np.argmax(yt, axis=1)
#print(accuracy_score(rounded_test, rounded_prediction))
