# import libraries

import boto3, re, sys, math, json, os, sagemaker, urllib.request

from sagemaker import get_execution_role

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from IPython.display import Image                

from IPython.display import display              

from time import gmtime, strftime                

from sagemaker.predictor import csv_serializer

import nltk
nltk.download('nps_chat')
nltk.download('punkt')

# Define IAM role

role = sagemaker.get_execution_role()

s3 = boto3.resource('s3')

bucket = 'ad440-mpg-floop-export-storage'

obj = s3.Object(bucket, 'auto-floop-s3-export3-sagemaker.json')

s3_client = boto3.client('s3')
client = boto3.client('sagemaker')
data = json.load(obj.get()['Body'])
print(data[0])

# In[195]:

posts = nltk.corpus.nps_chat.xml_posts()[:10000]

Question_Words = [ "do i", "do you", "what", "who", "is it", "why","would you", "how","is there",
                    "are there", "is it so", "is this true" ,"to know", "is that true", "are we", "am i", 
                   "question is", "tell me more", "can i", "can we", "tell me", "can you explain",
                   "question","answer", "questions", "answers", "ask"]
interrog_verbs = ["is","am","can","are","do","does"]

listQuestions = []

# Create array of the sample sentences to analyze
sentences=[]

# switch dataList to data for get all data
for x in data:
    for y in x:       
        sentences.append(y['Text'])


# In[196]:


def post_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
         
    return features


# In[197]:


def perform_classification():
        featuresets = [(post_features(post.text), post.get('class')) for post in posts]
         
         
        training_size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[training_size:], featuresets[:training_size]
         
        classifier = nltk.NaiveBayesClassifier.train(train_set)
         
         
        return classifier
    
    
myclassifier= perform_classification()


# In[198]:


types = ["whQuestion","ynQuestion"]

def nltk_is_quest(ques):
    question_type = myclassifier.classify(post_features(ques)) 
    return question_type in types


# In[199]:


def is_question(question):
    question = question.lower().strip()
    if not nltk_is_quest(question):
        is_ques = False
        # check if any of pattern exist in sentence
        for pattern in Question_Words:
            is_ques  = pattern in question
            if is_ques:
                break

        # divide the sentence
        sentence_arr = question.split(".")
        for sentence in sentence_arr:
            if len(sentence.strip()):
                # test if sentence ends with "?" or a interrogative verb
                first_word = nltk.word_tokenize(sentence)[0]
                if sentence.endswith("?") or first_word in interrog_verbs:
                    is_ques = True
                    break
        return is_ques    
    else:
        return True


for j in sentences:
    changeStr = ' '.join([str(elem) for elem in j])
    check = is_question(changeStr)
    #if check == "NaN":
        #print(changeStr)
    listQuestions.append(check)


# In[200]:


df = pd.DataFrame(list(zip(sentences, listQuestions)),columns=['Sentence', 'Question'])


# In[201]:


#Pie chart for visualization
plt.pie(df['Question'].value_counts(), labels = df['Question'].value_counts().keys(), autopct='%.1f%%')
plt.show()


# In[202]:


#Test algorithm for accuracy
print(is_question("this is a test"))


# In[203]:


#Show results
df


# In[ ]: