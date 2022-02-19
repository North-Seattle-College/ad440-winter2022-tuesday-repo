import nltk
from nltk.corpus import nps_chat
 
Question_Words = [ 'where','how','why','did','do','does',"isn't",'has','am i', 'are','can','could','is','may',"can't", 
"didn't",'will','when',"doesn't","haven't",'have','what',"aren't",'would',"couldn't","wouldn't","won't","shouldn't",'should']
 
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
 
sent=input("Inter sentence: ")

    #input chat posts
    # 2. Tokenize sentences using NLTK's word_tokenize
    # return dict of tokenized words

def post_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
         
    return features

#feature=dialogue_act_features(posts)

    #Input: none
    #  1. Divide data into 80% training and 10% testing sets
    # 2. Use NLTK's Multinomial Naive Bayes to perform classifcation    
    # Return: Classifier object

def __perform_classification():
        featuresets = [(post_features(post.text), post.get('class')) for post in posts]
         
        #print(f)
        training_size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[training_size:], featuresets[:training_size]
         
        classifier = nltk.NaiveBayesClassifier.train(train_set)
         
        #$print(classifier)
        return classifier
 
 
 
cl= __perform_classification()
 

types = ["whQuestion","ynQuestion","Statement"]
# Input a sentence
# returns the type sentence
def is_ques(ques):
    question_type = cl.classify(post_features(ques)) 
     
    return  question_type
    
 

    # Method : IsQuestion
    # Input: Sentence to be predicted
    # Return: type of sentence it is using nltk  
def IsQuestion(sentence):
    type=is_ques(sentence)
    #print("type is"+type) 
    first_word = sentence.split()[0].lower()  
     
    
    if  ((type=="whQuestion" or type== "ynQuestion") or (first_word in Question_Words ))  :
             
        print("This is a question")
                                 
    elif type=="Other" or type== "Reject":
         print("This is garbled text")   

    else:        
        print("This is a statement") 
         
  
IsQuestion(sent)