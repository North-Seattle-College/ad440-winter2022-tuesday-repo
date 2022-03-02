import string

import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

print('Libraries imported.')

import pandas as pd


# Reading the Json file and convert to an list.


path = input("Enter the file Path:")
dataset = pd.read_json(path).values.tolist()
print('Dataset imported')


def clean_dataset(dataset):
    
    new_ds = map(lambda x: x[0].lower(),dataset)    

    return list(new_ds)


new_ds = clean_dataset(dataset)
print('Cleaned dataset')



def sentiment_analyse(sentiment_text):
#     print('{}: '.format(sentiment_text), end = '')
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        return 'Negative'
    elif score['neg'] < score['pos']:
        return 'Positive'
    else:
        return 'Neutral'


# Define an list
sentiments = []
for i in new_ds:
    sentiments.append(sentiment_analyse(i))





result = pd.DataFrame({'Original Data':dataset, 'Sentiment Identified':sentiments})


result.to_csv('results.csvv')

print(result)

print(result['Sentiment Identified'].value_counts())
plt.pie(result['Sentiment Identified'].value_counts(), labels = result['Sentiment Identified'].value_counts().keys(), autopct='%.1f%%')
plt.show()