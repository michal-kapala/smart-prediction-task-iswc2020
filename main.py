import os
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


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


def prepare_dataset_wd(df):
    type_df = pd.DataFrame(df['type'].tolist())
    type_df = pd.concat([df['id'].to_frame(), type_df], axis=1).set_index('id')
    type_df = type_df.stack().to_frame(name='type')
    type_df = pd.merge(df.drop('type', axis=1), type_df, on='id')
    type_df = pd.concat([type_df.drop('type', 1), pd.get_dummies(type_df.type).mul(int(1))], axis=1)

    return type_df


def tokenize(df):
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(df['question'])
    # create document term matrix
    df_dtm = pd.DataFrame(cv_matrix.toarray(), index=df['id'].values, columns=cv.get_feature_names())
    return df_dtm


dataset_wd = load_dataset("lcquad2_anstype_wikidata_train.json")
categories_wd = load_wikidata_categories()

dataset_wd_df = prepare_dataset_wd(pd.DataFrame(dataset_wd))
tokenized_wd_df = tokenize(dataset_wd_df)

print(categories_wd.head())
print(dataset_wd_df.head(10))
print(tokenized_wd_df)
#dataset_wd_df.to_csv('dataset_wd_df.csv')
