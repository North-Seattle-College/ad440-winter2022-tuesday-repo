exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log(event);
  console.log("----- lambda start");

  //createMessage(event);
  console.log("start if");
  if (event.body) {
    //  console.log(event);
    return createMessage(event);
  } else {
    return {
      statusCode: 400,
    };
  }
};
console.log("createMessage start");
function createMessage(event) {
  // body...
  // console.log("inside method");
  const body = JSON.parse(event.body);
  if (body.name === "")
    return {
      statusCode: 400,
      body: JSON.stringify({
        message: "Unsuccesfuly,empty string",
        details: body,
      }),
    };
  else if (body.name === "ping")
    return {
      statusCode: 201,
      body: JSON.stringify({
        message: "succesfuly, pong",
        details: body,
      }),
    };
  else if (body.name !== "ping" && body.name !== "")
    return {
      statusCode: 400,
      body: JSON.stringify({
        message: "Unsuccesfuly,not correct data",
        details: body,
      }),
    };

  //   const response = {
  //     statusCode: 201,
  //     body: JSON.stringify({
  //       message: "succesfuly",
  //       details: body
  //     })
  //   };
  // return response;
}
