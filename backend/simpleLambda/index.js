exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log(event);
  const response = {
    statusCode: 200,
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify("Hi!"),
  };
  //return response;
  callback(null, response);
};
