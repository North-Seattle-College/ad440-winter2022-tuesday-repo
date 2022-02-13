import nltk
from nltk.corpus import nps_chat
 
Question_Words = [ 'where', 'when','how',"couldn't",'why',"isn't",'did','do', 'have','am','is','are','can','could','may','would','should'
"didn't","doesn't","haven't","aren't", "can't","wouldn't","won't","shouldn't",'?']
 
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
 
sent=input("Inter sentence: ")

    #input chat posts
    # 2. Tokenize sentences using NLTK's word_tokenize
    # return dict of tokenized words

def dialogue_act_features(post):
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
        featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
        training_size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[training_size:], featuresets[:training_size]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
         
        return classifier
 
 
 
cl= __perform_classification()
 

types = ["whQuestion","ynQuestion","Statement"]
# Input a sentence
# returns the type sentence
def is_ques_using_nltk(ques):
    question_type = cl.classify(dialogue_act_features(ques)) 
     
    return  question_type

 

    # Method : IsQuestion
    # Input: Sentence to be predicted
    # Return: type of sentence it is using nltk  
def IsQuestion(sentence):
    type=is_ques_using_nltk(sentence)
    #print("type is"+type) 
       
    
    for pattern in Question_Words:
        if pattern in sentence.split()[0] or  type=="whQuestion" or type== "ynQuestion"  :
            print("This is a question")
            exit()                      
             
    else:        
        print("This is a statement") 
         
question="  are you smart"   
IsQuestion(sent)
 