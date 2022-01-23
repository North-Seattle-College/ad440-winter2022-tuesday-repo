exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log(event);
  const response = {
    metood: "post",
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify([
      {
        id: 1,
        name: "TI",
        description: "Hi from Lambda! ID# 1",
      },
      { id: 2, name: "Kl", description: "Hi from Lambda! ID# 2" },
    ]),
  };
  //return response;
  callback(null, response);
};
