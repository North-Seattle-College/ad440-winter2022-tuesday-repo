import string
import nltk
import json
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
import pandas as pd
import boto3
import botocore
# !pip install sagemaker
import sagemaker
from sagemaker import get_execution_role

sagemaker_session = sagemaker.Session()
role = "christopher.navocz1@seattlecolleges.edu"
bucket_name = 'deploy-sagemaker-conversation'

s3_url = 's3://deploy-sagemaker-conversation/floop_data_15k.json'
conn = boto3.client('s3')
contents = conn.list_objects(Bucket = bucket_name)['Contents']

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
# s3_client.list_objects(Bucket = bucket_name)['Contents']
dataset = conn.get_object(Bucket = bucket_name, Key = 'floop_data_15k.json')
s3_client.get_object(Bucket = bucket_name, Key = 'floop_data_15k.json')

path = "floop_data_15k.json"
dataset = pd.read_json(path).values.tolist()

def clean_dataset(dataset):

    new_ds = map(lambda x: x[0].lower(),dataset)    

    return list(new_ds)


new_ds = clean_dataset(dataset)

def sentiment_analysis(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        return 'Negative'
    elif score['neg'] < score['pos']:
        return 'Positive'
    else:
        return 'Neutral'

sentiments = []
for i in new_ds:
    sentiments.append(sentiment_analysis(i))

result = pd.DataFrame({'Original Data':dataset, 'Sentiment Identified':sentiments})

result.to_csv('results.csv')

print(result)

print(result['Sentiment Identified'].value_counts())
plt.pie(result['Sentiment Identified'].value_counts(), labels = result['Sentiment Identified'].value_counts().keys(), autopct='%.1f%%')
plt.show() 