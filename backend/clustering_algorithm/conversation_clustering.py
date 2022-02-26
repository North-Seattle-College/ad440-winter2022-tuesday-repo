import json
import os.path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


# return a simplified xy dict, with just the values we need for K-means clustering
def define_xy(df):
    y = df['comparison_metric'].values
    X = df['length_of_thread'].values
    return {'y': y.reshape(-1, 1), 'X': X.reshape(-1, 1)}


# split the data into test sets and train sets, 80/20
def test_train_split(xy_dict):
    X_train, X_test, y_train, y_test = train_test_split(xy_dict['X'], xy_dict['y'],
                                                        test_size=0.2, random_state=42,
                                                        stratify=xy_dict['y'])
    return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}


# we'll fill this out when we know what it is in the thread we want to correlate with length
def get_metric_from_thread(thread):
    return 0


# won't give us a usable prediction until we have a correlation metric
def build_classifier(xy_dict):
    knn = KNeighborsClassifier(n_neighbors=6)
    knn.fit(xy_dict['X'], xy_dict['y'])
    y_pred = knn.predict(xy_dict['X'])
    print("Prediction: {}".format(y_pred))


if __name__ == '__main__':
    # 2 dictionaries so that we don't operate on the comments dictionary
    file_path = input("Please enter filepath to floop data: ")
    if not os.path.exists(file_path):
        raise FileNotFoundError("Invalid entry for file path")
    comments_dict = json.load(open(file_path, "r"))
    # count number of comments in each conversation
    counts_dict = {}
    for thread in comments_dict:
        length = len(thread)
        if counts_dict.get(length):
            counts_dict[length] = int(counts_dict[length]) + 1
        else:
            counts_dict[length] = 1

    # build an array of dictionaries to process next steps
    parsed_data_array = [{"thread": str(thread), "comparison_metric": get_metric_from_thread(thread),
                          "length_of_thread": len(thread), "conversations_with_same_len": counts_dict.get(len(thread))}
                         for thread in comments_dict]

    # build a dataframe, and plot it so that we can see the "clusters" of the distribution of conversation lengths
    df = pd.DataFrame(parsed_data_array)
    df.plot.scatter(x="length_of_thread", y="conversations_with_same_len", s=100)
    plt.show()

    build_classifier(define_xy(df))

