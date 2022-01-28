from SPARQLWrapper import JSON
from helper import sparql2df_entities, sparql2df_types

# Query for entities which are 'instance-of' of id type
def get_entity_urls_for_type(sparql, type_id):
    sparql.setQuery(
    '''
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    ''' +
    'SELECT DISTINCT ?item ?itemLabel WHERE { ?item wdt:P31 ' +
    f'{type_id}. ' +
    'SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } } LIMIT 10'
    )

    sparql.setReturnFormat(JSON)
    qresult = sparql.query().convert()
    df = sparql2df_entities(qresult)
    return df['value']

# Query for entity types of an object specified by the url
# example url: http://www.wikidata.org/entity/Q34172
def get_types_for_entity_url(sparql, url):
    sparql.setQuery(
        '''
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        ''' +
        'SELECT DISTINCT ?itemType WHERE { '+
        f'<{url}> wdt:P31 ?itemType.' +
        '} LIMIT 10'
    )
    sparql.setReturnFormat(JSON)
    qresult = sparql.query().convert()
    df = sparql2df_types(qresult)
    return df['type']

# Query for entity types of an object specified by wikidata id
# example url: http://www.wikidata.org/entity/Q34172
def get_types_for_entity_id(sparql, id):
    sparql.setQuery(
        '''
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        ''' +
        'SELECT DISTINCT ?itemType WHERE { '+
        f'<http://www.wikidata.org/entity/{id}> wdt:P31 ?itemType.' +
        '} LIMIT 10'
    )
    sparql.setReturnFormat(JSON)
    qresult = sparql.query().convert()
    df = sparql2df_types(qresult)
    return df['type']

