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
    // var x= feedback.split(".");
    var sent = [];
    var buf = "";
    for (var i = 0; i < feedback.length; i++) {
      buf += feedback[i];
      if (feedback[i] == ".") {
        sent.push(buf);
        buf = "";
        // x[i] += " ";
      } else if (feedback[i] == "?") {
        sent.push(buf);
        buf = "";
      } else if (feedback[i] == "!") {
        sent.push(buf);
        buf = "";
      }
    }
    if (buf.length > 0) sent.push(buf);
  }

  let FeedBack = `${sent}.`;

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
