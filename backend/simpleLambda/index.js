//TODO: Connect DynamoDB destination
const AWS = require("aws-sdk");
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
    let body;
    let statusCode=200;
    const headers = {
        "Content-Type": "application/json"
    };

    try {
        // break up sentences
        let feedback = event.feedback;
        let sentenceArray = [];
        let sentenceObject = {};
        let newSentence = "";
        for (let i = 0; i < feedback.length; i++) {
            newSentence = newSentence + feedback[i];
            if (feedback[i] == "." || feedback[i] == "?" || feedback[i] == "!") {
                
                // add sentence string
                sentenceObject.sentence = newSentence;
                
                // determine sentence type
                switch (feedback[i]) {
                    case ".":
                        sentenceObject.type = "statement";
                        break;
                    case "?":
                        sentenceObject.type = "question";
                        break;
                    case "!":
                        sentenceObject.type = "exclamation";
                        break;
                }
                
                // determine sentence sentiment
                if (newSentence.search("good") > 0) {
                    sentenceObject.sentiment = "positive";
                } else if (newSentence.search("bad") > 0) {
                    sentenceObject.sentiment = "negative";
                } else {
                    sentenceObject.sentiment = "neutral";
                }
                
                // add object to array
                sentenceArray.push(sentenceObject);
                
                // reset 
                newSentence = "";
            }
        }
        // check if the array is empty
        if (sentenceArray.length == 0) {
            sentenceObject.sentence = "No full sentences detected. Sentences must end with punctuation of either a period (.), exclamation point (!), or question mark (?), to be considered full sentences."
            sentenceObject.type = "No full sentences detected to detect type. Sentences must end with punctuation of either a period (.), exclamation point (!), or question mark (?), to be considered full sentences.";
            sentenceObject.sentiment = "No full sentences detected to determine sentiment. Sentences must end with punctuation of either a period (.), exclamation point (!), or question mark (?), to be considered full sentences.";
            sentenceArray.push(sentenceObject);
        }
        // return JSON array of sentences
        body = sentenceArray;
        
    } catch (err) {
        statusCode = 400;
        body = err.message;
    } finally {
        body = JSON.stringify(body)
    }
    
    return {
        statusCode,
        body,
        headers
};
};