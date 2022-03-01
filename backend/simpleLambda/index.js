//TODO: Connect DynamoDB destination
const AWS = require("aws-sdk");
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
    let body;
    let statusCode=200;
    console.log(event)
    const headers = {
        "Content-Type": "application/json"
    };

    try {
        // break up sentences
        body = event.feedback;
        let sentenceArray = [];
        let feedback = event.feedback;
        let newSentence = "";
        for (let i = 0; i < feedback.length; i++) {
            newSentence = newSentence + feedback[i];
            if (feedback[i] == "." || feedback[i] == "?" || feedback[i] == "!") {
                let sentenceObject = {};
                
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
        console.log(sentenceArray);
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