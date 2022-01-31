//let mes= event["hi"];
exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log("----- lambda start");
  console.log(event);

  console.log("start if");
  if (event.httpMethod === "post") {
    console.log(event);
    return createMessage(event);
  }
};
console.log("createMessage start");
function createMessage(event) {
  // body...
  const body = JSON.parse(event.body);
  const response = {
    statusCode: 201,
    body: JSON.stringify({
      message: "succesfuly",
      details: body,
    }),
  };
  return response;
}
