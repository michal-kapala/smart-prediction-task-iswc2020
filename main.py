import pandas as pd
import string
import nltk
from SPARQLWrapper import SPARQLWrapper
from nltk.corpus import stopwords
from helper import *
from queries import *



# Config
pd.set_option('display.width', 50)
dataset_file = "lcquad2_anstype_wikidata_train.json"
is_dbpedia = True if (dataset_file.find("dbpedia") >= 0) else False
sparql_endpoint = "https://query.wikidata.org/sparql" if is_dbpedia == False else "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(sparql_endpoint)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
stop_words = set(stopwords.words('english')) - {'what', 'which', 'whose', 'why', 'when', 'where', 'who'}
table = str.maketrans('','', string.punctuation)

# ETL
dataset_df = load_dataset(dataset_file, is_dbpedia)
# For performance and wikidata api 429 'Too Many Requests' response reasons
dataset_df = dataset_df.head(5)
categories = load_wikidata_categories()

# Question text preprocessing
tokens_column = []
question_words_column = []
postags_column = []

for index, row in dataset_df.iterrows():
    question = row['question']
    tokens = tokenize(question, stop_words, table)
    tokens_column.append(tokens)
    question_words_column.append(find_question_word(tokens))
    postags_column.append(nltk.pos_tag(tokens))

dataset_df['ordered_tokens'] = tokens_column
dataset_df['question_word'] = question_words_column
dataset_df['pos_tags'] = postags_column
print(dataset_df)

# Select the words for SPARQL querying
qcandidates = []
for index, row in dataset_df.iterrows():
    # Search for questions about resource type
    if row['category'] == 'resource':
        candidate_tokens = []
        for token in row['ordered_tokens']:
            # Qualify the token if it is a noun or verb
            if token != row['question_word'] and is_noun(token, row['pos_tags']):
                candidate_tokens.append(token)
        qcandidates.append(candidate_tokens)
    # Ignore literal and boolean questions processing
    else:
        qcandidates.append([])

dataset_df['candidates'] = qcandidates
print(dataset_df)

# Get candidates Wikidata IDs (Q-items) from categories set
qitems_column = []
for index, row in dataset_df.iterrows():
    # Search for potentially non-empty candidate lists
    if row['category'] == 'resource':
        qitems = []
        # For every candidate
        if(row['candidates'] != []):
            for c in row['candidates']:
                # Search through category descriptions
                for index2, cat_row in categories.iterrows():
                    # If the candidate is found in the description, save the qitem id
                    if cat_row['category'].find(c) > -1 or cat_row['category'].find(c.lower()) > -1:
                        qitems.append(cat_row['wiki_id'])
        # Remove duplicate ids for the same question
        qitems = list(dict.fromkeys(qitems))
        qitems_column.append(qitems)
    # Ignore other questions
    else:
        qitems_column.append([])

dataset_df['cand_qitems'] = qitems_column
print(dataset_df)

# SPARQL queries
cand_types_column = []
for index, row in dataset_df.iterrows():
    if row['cand_qitems'] != []:
        cand_types = []
        for id in row['cand_qitems']:
            # A single query can return multiple matches
            res = get_types_for_entity_id(sparql, id)
            cand_types.extend(res)
        cand_types = list(dict.fromkeys(cand_types))
        cand_types_column.append(cand_types)
    else:
        cand_types_column.append([])

dataset_df['cand_types'] = cand_types_column

print(dataset_df)

dataset_df.to_json(r'.\results.json')

# Query examples

# Query for entities which are 'instance-of' of type_id
# Example type_id: wd:Q7889
# print(get_entity_urls_for_type(sparql, "wd:Q7889"))

# Query for entity types of an object specified by the url
# Example url: http://www.wikidata.org/entity/Q34172
# print(get_types_for_entity_url(sparql, 'http://www.wikidata.org/entity/Q34172'))
