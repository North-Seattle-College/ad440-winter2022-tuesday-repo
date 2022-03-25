exports.handler = async (event) => {
  let feedback = "";
  let responseCode = 200;

  if (event.body !== "") {
    let body;
    try {
      body = JSON.parse(event.body);
    } catch (e) {
      body = { message: "some thing wrong" };
    }

    feedback = body.feedback;

    var sentence = [];
    var storeSentece = "";
    for (var i = 0; i < feedback.length; i++) {
      storeSentece += feedback[i];
      if (feedback[i] == ".") {
        sentence.push(storeSentece);
        storeSentece = "";
      } else if (feedback[i] == "?") {
        sentence.push(storeSentece);
        storeSentece = "";
      } else if (feedback[i] == "!") {
        sentence.push(storeSentece);
        storeSentece = "";
      }
    }
    if (storeSentece.length > 0) sentence.push(storeSentece);
  }

  let FeedBack = sentence;

  let responseBody = {
    sentence: FeedBack,
    // input: event
  };

  let response = {
    statusCode: responseCode,

    body: JSON.stringify(responseBody),
  };

  return response;
};
