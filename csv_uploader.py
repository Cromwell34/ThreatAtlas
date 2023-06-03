from elasticsearch import Elasticsearch, helpers
import pandas as pd

# Connect to the Elasticsearch instance
es = Elasticsearch('https://localhost:9200')

# Define the name of the Elasticsearch index
index_name = 'my_index'

# Define the path to the CSV file
csv_path = input("insert filename: ")

# Load the CSV data into a Pandas DataFrame
data = pd.read_csv(csv_path)

# Convert the DataFrame to a list of dictionaries
docs = data.to_dict('records')

# Define the Elasticsearch index mapping
mapping = {
    'mappings': {
        'properties': {
            "@timestamp": { "type": "date"},
            "ActionGeo_ADM1Code": { "type": "keyword"},
            "ActionGeo_CountryCode": {"type": "keyword"},
            "ActionGeo_FeatureID": { "type": "keyword"},
            "ActionGeo_FullName": { "type": "keyword"},
            "ActionGeo_Lat": {"type": "double"},
            "ActionGeo_Long": {"type": "double"},
            "ActionGeo_Type": {"type": "long"},
            "Actor1Code": {"type": "keyword"},
            "Actor1CountryCode": {"type": "keyword"},
            "Actor1Geo_ADM1Code": {"type": "keyword"},
            "Actor1Geo_CountryCode": {"type": "keyword"},
            "Actor1Geo_FeatureID": {"type": "keyword"},
            "Actor1Geo_FullName": {"type": "keyword"},
            "Actor1Geo_Lat": { "type": "double"},
            "Actor1Geo_Long": {"type": "double"},
            "Actor1Geo_Type": {"type": "long"},
            "Actor1KnownGroupCode": {"type": "keyword"},
            "Actor1Name": {"type": "keyword"},
            "Actor1Religion1Cod": {"type": "keyword"},
            "Actor1Religion2Code": {"type": "keyword"},
            "Actor1Type1Code": {"type": "keyword"},
            "Actor1Type2Code": {"type": "keyword"},
            "Actor2Code": {"type": "keyword"},
            "Actor2CountryCode": {"type": "keyword"},
            "Actor2EthnicCode": {"type": "keyword"},
            "Actor2Geo_ADM1Code": {"type": "keyword"},
            "Actor2Geo_CountryCode": {"type": "keyword"},
            "Actor2Geo_FeatureID": {"type": "keyword"},
            "Actor2Geo_FullName": {"type": "keyword"},
            "Actor2Geo_Lat": {"type": "double"},
            "Actor2Geo_Long": {"type": "double"},
            "Actor2Geo_Type": {"type": "long"},
            "Actor2KnownGroupCode": {"type": "keyword"},
            "Actor2Name": {"type": "keyword"},
            "Actor2Religion1Code": {"type": "keyword"},
            "Actor2Type1Code": {"type": "keyword"},
            "Actor2Type2Code": {"type": "keyword"},
            "AvgTone": {"type": "double"},
            "DATEADDED": {"type": "long"},
            "EventBaseCode": {"type": "long"},
            "EventCode": {"type": "long"},
            "EventRootCode": {"type": "long"},
            "FractionDate": {"type": "double"},
            "GLOBALEVENTID": {"type": "date", "format": "epoch_second"},
            "GoldsteinScale": {"type": "double"},
            "IsRootEvent": {"type": "long"},
            "MonthYear": {"type": "long"},
            "NumArticles": {"type": "long"},
            "NumMentions": {"type": "long"},
            "NumSources": {"type": "long"},
            "QuadClass": {"type": "long"},
            "SOURCEURL": {"type": "keyword"},
            "SQLDATE": {"type": "long"},
            "Year": {"type": "long"},
            "column1": {"type": "long"}
            }
    }
}

# Create the Elasticsearch index with the mapping
es.indices.create(index=index_name, body=mapping)

# Index the CSV data in Elasticsearch
for doc in docs:
    es.index(index=index_name, body=doc)


#   "properties": {
#     "@timestamp": { "type": "date"},
#     "ActionGeo_ADM1Code": { "type": "keyword"},
#     "ActionGeo_CountryCode": {"type": "keyword"},
#     "ActionGeo_FeatureID": { "type": "keyword"},
#     "ActionGeo_FullName": { "type": "text"},
#     "ActionGeo_Lat": {"type": "double"},
#     "ActionGeo_Long": {"type": "double"},
#     "ActionGeo_Type": {"type": "long"},
#     "Actor1Code": {"type": "keyword"},
#     "Actor1CountryCode": {"type": "keyword"},
#     "Actor1Geo_ADM1Code": {"type": "keyword"},
#     "Actor1Geo_CountryCode": {"type": "keyword"},
#     "Actor1Geo_FeatureID": {"type": "keyword"},
#     "Actor1Geo_FullName": {"type": "text"},
#     "Actor1Geo_Lat": { "type": "double"},
#     "Actor1Geo_Long": {"type": "double"},
#     "Actor1Geo_Type": {"type": "long"},
#     "Actor1KnownGroupCode": {"type": "keyword"},
#     "Actor1Name": {"type": "keyword"},
#     "Actor1Religion1Cod": {"type": "keyword"},
#     "Actor1Religion2Code": {"type": "keyword"},
#     "Actor1Type1Code": {"type": "keyword"},
#     "Actor1Type2Code": {"type": "keyword"},
#     "Actor2Code": {"type": "keyword"},
#     "Actor2CountryCode": {"type": "keyword"},
#     "Actor2EthnicCode": {"type": "keyword"},
#     "Actor2Geo_ADM1Code": {"type": "keyword"},
#     "Actor2Geo_CountryCode": {"type": "keyword"},
#     "Actor2Geo_FeatureID": {"type": "keyword"},
#     "Actor2Geo_FullName": {"type": "text"},
#     "Actor2Geo_Lat": {"type": "double"},
#     "Actor2Geo_Long": {"type": "double"},
#     "Actor2Geo_Type": {"type": "long"},
#     "Actor2KnownGroupCode": {"type": "keyword"},
#     "Actor2Name": {"type": "keyword"},
#     "Actor2Religion1Code": {"type": "keyword"},
#     "Actor2Type1Code": {"type": "keyword"},
#     "Actor2Type2Code": {"type": "keyword"},
#     "AvgTone": {"type": "double"},
#     "DATEADDED": {"type": "long"},
#     "EventBaseCode": {"type": "long"},
#     "EventCode": {"type": "long"},
#     "EventRootCode": {"type": "long"},
#     "FractionDate": {"type": "double"},
#     "GLOBALEVENTID": {"type": "date", "format": "epoch_second"},
#     "GoldsteinScale": {"type": "double"},
#     "IsRootEvent": {"type": "long"},
#     "MonthYear": {"type": "long"},
#     "NumArticles": {"type": "long"},
#     "NumMentions": {"type": "long"},
#     "NumSources": {"type": "long"},
#     "QuadClass": {"type": "long"},
#     "SOURCEURL": {"type": "keyword"},
#     "SQLDATE": {"type": "long"},
#     "Year": {"type": "long"},
#     "column1": {"type": "long"
#     }