#Using Python this is a non-working rough draft of a Lambda function that calls
#to breakFeedbackInSentence lambda, QuestionAnalysis lambda, and se_85400(The sentiment analysis lambda)

#import modules
import json
import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    
    invokeLan = boto3.client('lambda',region_name="us-west-2")
    
    #test in json format
    payload = {'feedback':'hello this is a test'}
    
    #call the sentence splitting algorithm
    resp = client.invoke(FunctionName= 'arn:aws:lambda:us-west-2:061431082068:function:breakFeedbackInSentence', InvocationType='RequestResponse', Payload=json.dumps(payload))
    
    #call isquestion /not question algorithm
    isques = client.invoke(FunctionName= 'arn:aws:lambda:us-west-2:061431082068:function:QuestionAnalysis', InvocationType='RequestResponse', Payload=json.dumps(payload))
    
    #call sentiment analysis algorithm
    senti = client.invoke(FunctionName= 'arn:aws:lambda:us-west-2:061431082068:function:se_85400', InvocationType='RequestResponse', Payload=json.dumps(payload))
    
    #String to return total value
    
    sentence = "sentence: " + resp + "isQuestion: " + isques + "Sentiment: " + senti 
    
    return sentence