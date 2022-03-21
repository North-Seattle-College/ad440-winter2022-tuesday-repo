exports.handler = async (event) => {
  console.log("event: " + JSON.stringify(event));
  console.log("----- lambda start");
  let feedBack = "Good Job!";


  let responseCode = 201;
  console.log("event: " + JSON.stringify(event));

  if (event.body) {
    let body = JSON.parse(event.body);
    if (body.feedBack === "")
      return {
        statusCode: 400,
      };
    else feedBack = body.feedBack;
  }

  let FeedBack = `Teacher feed back:  ${feedBack}.`;

  let responseBody = {
    message: FeedBack,
    // input: event
  };

  let response = {
    statusCode: responseCode,

    body: JSON.stringify(responseBody),
  };

  return response;
};
