import os
import json
import pandas as pd
from nltk.tokenize import word_tokenize



# loads a JSON dataset into a DataFrame
def load_dataset(filename, is_dbpedia):
    root_dir = os.path.dirname(__file__)
    sub_folder = "DBpedia" if is_dbpedia else "Wikidata"
    dir = os.path.join(root_dir + f"\\{sub_folder}")
    dir = os.path.join(dir, filename)
    file = open(dir, encoding="UTF-8")
    # formerly wrapped with prepare_dataset_wd()
    return pd.DataFrame(json.load(file)) 


# loads ontology classes list as pd.DataFrame
def load_wikidata_categories():
    root_dir = os.path.dirname(__file__)
    dir = os.path.join(root_dir + "\\Wikidata\\wikidata__qid_label.csv")
    file = open(dir, encoding="utf8")
    return pd.read_csv(file, delimiter="|", names=['wiki_id', 'category'])


# Converts the dataset to DataFrame
def prepare_dataset_wd(df):
    type_df = pd.DataFrame(df['type'].tolist())
    type_df = pd.concat([df['id'].to_frame(), type_df], axis=1).set_index('id')
    type_df = type_df.stack().to_frame(name='type')
    type_df = pd.concat([type_df.drop('type', axis=1), pd.get_dummies(type_df.type).mul(int(1))], axis=1)
    type_df = type_df.groupby(level=0, axis=0).sum()
    type_df = pd.merge(df.drop('type', axis=1), type_df, on='id')

    return type_df


# Tokenizes all questions (question's word order is lost)
def tokenize(text, stops, table):
    text = word_tokenize(text)
    text = [w.translate(table) for w in text]
    text = [w for w in text if w.isalpha()]
    text = [w for w in text if not w in stops]
    text = [w.capitalize() for w in text]
    return text


# Converts SPARQL query to custom DataFrame for get_entities query
def sparql2df_entities(qresult):
    df = pd.DataFrame(columns=['type', 'value', 'desc'])
    id = 0
    for row in qresult['results']['bindings']:
        df.loc[id] = pd.Series({
            'type':row['item']['type'],
            'value': row['item']['value'],
            'desc': row['itemLabel']['value']
        })
        id+=1
    return df

# Converts SPARQL query to custom DataFrame for get_types query
def sparql2df_types(qresult):
    df = pd.DataFrame(columns=['type'])
    id = 0
    for row in qresult['results']['bindings']:
        df.loc[id] = pd.Series({
            'type':row['itemType']['value'],
        })
        id+=1
    return df

#Prints raw JSON from SPARQLWrapper
def print_raw_json(qresult):
    for res in qresult['results']['bindings']:
        print(res)
        # For entity querying:
        # print('Type: ' + res['itemLabel']['type'] + '\tValue: ' + res['itemLabel']['value'])