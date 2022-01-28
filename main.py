import numpy as np
import pandas as pd
from SPARQLWrapper import SPARQLWrapper
import string
import nltk
from nltk.corpus import stopwords

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from helper import *
from queries import *

# Config
dataset_file = "lcquad2_anstype_wikidata_train.json"
is_dbpedia = True if (dataset_file.find("dbpedia") >= 0) else False
sparql_endpoint = "https://query.wikidata.org/sparql" if is_dbpedia == False else  "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(sparql_endpoint)
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english')) - {'what', 'which', 'whose', 'why', 'when', 'where'}
table = str.maketrans('','', string.punctuation)

# ETL
dataset_df = load_dataset(dataset_file, is_dbpedia)
categories_wd = load_wikidata_categories()

# Question text preprocessing
tokens_column = []

for index, row in dataset_df.iterrows():
    question = row['question']
    tokens = tokenize(question, stop_words, table)
    tokens_column.append(tokens)

dataset_df['ordered_tokens'] = tokens_column
print(dataset_df)

# Query examples

# Query for entities which are 'instance-of' of type_id
# Example type_id: wd:Q7889
# print(get_entity_urls_for_type(sparql, "wd:Q7889"))

# Query for entity types of an object specified by the url
# Example url: http://www.wikidata.org/entity/Q34172
# print(get_types_for_entity_url(sparql, 'http://www.wikidata.org/entity/Q34172'))



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
