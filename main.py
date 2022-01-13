import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


# loads a JSON dataset
def load_dataset(filename):
    is_dbpedia = True if (filename.find("dbpedia") >= 0) else False
    root_dir = os.path.dirname(__file__)
    sub_folder = "DBpedia" if is_dbpedia else "Wikidata"
    dir = os.path.join(root_dir + f"\\{sub_folder}")
    dir = os.path.join(dir, filename)
    file = open(dir, encoding="UTF-8")
    return json.load(file)


# loads ontology classes list as pd.DataFrame
def load_wikidata_categories():
    root_dir = os.path.dirname(__file__)
    dir = os.path.join(root_dir + "\\Wikidata\\wikidata__qid_label.csv")
    file = open(dir, encoding="utf8")
    return pd.read_csv(file, delimiter="|")


def prepare_dataset_wd(df):
    type_df = pd.DataFrame(df['type'].tolist())
    type_df = pd.concat([df['id'].to_frame(), type_df], axis=1).set_index('id')
    type_df = type_df.stack().to_frame(name='type')
    type_df = pd.concat([type_df.drop('type', axis=1), pd.get_dummies(type_df.type).mul(int(1))], axis=1)
    type_df = type_df.groupby(level=0, axis=0).sum()
    type_df = pd.merge(df.drop('type', axis=1), type_df, on='id')

    return type_df


def tokenize(df):
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(df['question'])
    df_dtm = pd.DataFrame(cv_matrix.toarray(), index=df['id'].values, columns=cv.get_feature_names())
    return df_dtm


dataset_wd = load_dataset("lcquad2_anstype_wikidata_train.json")
categories_wd = load_wikidata_categories()                      # Numery i nazwy kategorii

dataset_wd_df = prepare_dataset_wd(pd.DataFrame(dataset_wd))    # id pytania / pytanie / kategoria / typy
dataset_wd_df_empty = dataset_wd_df.iloc[0:0]                   # same nagłówki
tokenized_wd_df = tokenize(dataset_wd_df)                       # id pytania / ztokenizowane pytanie
tokenized_wd_df_empty = tokenized_wd_df.iloc[0:0]               # same nagłówki
dataset_wd_df = dataset_wd_df.drop(columns=["question"])        # dataset_wd_df bez pytania

X = dataset_wd_df.drop(['id', 'category_x'], axis=1).to_numpy()
y = tokenized_wd_df.to_numpy()

clf = RandomForestClassifier(max_depth=2, n_estimators=20, verbose=2)
clf.fit(X, y)

#Testowy dataset
test_wd = load_dataset("lcquad2_anstype_wikidata_test_gold.json")

test_wd_df = prepare_dataset_wd(pd.DataFrame(test_wd))
test_wd_df = dataset_wd_df_empty.append(test_wd_df, sort=False)
token_test_wd_df = tokenize(test_wd_df)
token_test_wd_df = tokenized_wd_df_empty.append(token_test_wd_df, sort=False).fillna(0)
test_wd_df = test_wd_df.drop(columns=["question"]).fillna(0)

Xt = test_wd_df.drop(['id', 'category'], axis=1).to_numpy()
yt = token_test_wd_df.to_numpy()
Xt = Xt[:, :X.shape[1]]
yt = yt[:, :y.shape[1]]

prediction = clf.predict(Xt)

rounded_prediction = np.argmax(prediction, axis=1)
rounded_test = np.argmax(yt, axis=1)
print(accuracy_score(rounded_test, rounded_prediction))
