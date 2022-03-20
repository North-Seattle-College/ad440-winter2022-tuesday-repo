import json
import nltk
import text2emotion as te
from tokenizer import Tokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', download_dir="/tmp")
nltk.download('omw-1.4', download_dir="/tmp")

def sentiment_analysis(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        return 'Negative'
    elif score['neg'] < score['pos']:
        return 'Positive'
    else:
        return 'Neutral'    

def lambda_handler(event, context):
    # TODO implement
    data = event.copy()    
    data['sentiment'] =  sentiment_analysis(data['sentence'])
    print(data)
    return data
