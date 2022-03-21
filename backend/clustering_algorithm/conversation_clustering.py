import json
import os.path
import re

import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

def download_nltk_deps():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('vader_lexicon')


def insights_from_threads_of_one(comments_list):
    single_comment_threads = filter(lambda thread: len(thread) == 1, comments_list)
    single_comment_threads_parsed = [{"comment": str(comment[0]["Text"].strip()), "length_of_comment": len(comment[0]["Text"].strip()),
                                      "sentiment_score": get_sentiment_score(comment[0]["Text"])}
                                     for comment in single_comment_threads]
    df = pd.DataFrame(single_comment_threads_parsed)



    print("The comment with the `most positive sentiment` in this set is: " + str(df.iloc[df["sentiment_score"].idxmax()]["comment"]))
    print("The comment with the `most negative sentiment` in this set is: " + str(df.iloc[df["sentiment_score"].idxmin()]["comment"]))


    scores = df["sentiment_score"]
    comment_len = df["length_of_comment"]
    print("The modal sentiment score is: " + str(scores.mode()))
    print("The mean sentiment score is: " + str(scores.mean()))
    print("The median sentiment score is: " + str(scores.median()))
    print("Standard deviation from the mean of sentiment scores for threads containing one comment: "
          + str(scores.std()))

    print()
    print()
    print("The mean length of comment in single comment threads is: " + str(comment_len.mean()))
    print("The median length comment in single comment threads is: " + str(comment_len.median()))
    print("Standard deviation from the mean of sentiment scores for threads containing one comment: "
          + str(comment_len.std()))
    print()
    print()

    return len(df["comment"])

def get_sentiment_score(comment):
    lemmatizer = WordNetLemmatizer()
    eng_stop_words = stopwords.words('english')
    comment_lowered = str(comment).lower()
    comment_lowered_processed = re.sub('[^a-zA-Z]+', ' ', comment_lowered).strip()
    tokens = word_tokenize(comment_lowered_processed)
    words = [t for t in tokens if t not in eng_stop_words]
    lemmatized_words = [lemmatizer.lemmatize(w) for w in words]
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment_score = 0
    for word in lemmatized_words:
        sentiment_score += sentiment_analyzer.polarity_scores(word)["compound"]
    return sentiment_score

if __name__ == '__main__':
    download_nltk_deps()
    # 2 dictionaries so that we don't operate on any single comments dictionary
    file_path = input("Please enter file path to floop dataset: ")
    if not os.path.exists(file_path):
        raise FileNotFoundError("Invalid entry for file path")
    comments_list = json.load(open(file_path, "r"))

    # count number of comments in each conversation
    counts_dict = {}
    for thread in comments_list:
        length = len(thread)
        if counts_dict.get(length):
            counts_dict[length] = int(counts_dict[length]) + 1
        else:
            counts_dict[length] = 1

    number_of_single_comment_threads = insights_from_threads_of_one(comments_list)

    print("Proportion of threads with single comment: " + str(number_of_single_comment_threads) + "/"
          + str(len(comments_list)))



