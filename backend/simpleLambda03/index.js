exports.handler = async (event) => {
  console.log("event: " + JSON.stringify(event));
  console.log("----- lambda start");
  let feedBack = "";
  let responseCode = 201;

  if (event.body) {
    let body = JSON.parse(event.body);
    if (body.feedBack === "")
      return {
        statusCode: "400",
        body: JSON.stringify({ Error: "Empty feed back!" }),
      };
    else if (!body.feedBack)
      return {
        statusCode: "400",
        body: JSON.stringify({ Error: "info not matched" }),
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
