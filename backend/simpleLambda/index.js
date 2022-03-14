exports.handler = async (event) => {

 let feedback = "";
 let responseCode = 201;


  if (event.body !== "") {
    let body;
    try {
      body = JSON.parse(event.body);
    } catch (e) {
      body = { message: "dd" };
    }

    if (event.feedback === "null" || event.feedback === "undefined")
      return {
        statusCode: "400",
        body: JSON.stringify({ Error: " feed back undefined! or null!" }),
      };
    else if (body.feedback === "")
      return {
        statusCode: "400",
        body: JSON.stringify({ Error: "Missing feedback string" }),
      };
    else if (!body.feedback)
      return {
        statusCode: "400",
        body: JSON.stringify({ Error: "info not matched" }),
      };
    else feedback = body.feedback;
   }
 
  let FeedBack = `Teacher feed back:  ${feedback}.`;

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
