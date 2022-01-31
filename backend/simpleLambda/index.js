const messafe='null'

exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log(event);
  const response = {
    metood: "post",
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event[body
      // {
      //   id: 1,
      //   name: "TI",
      //   description: "Hi from Lambda! ID# 1",
      // },
      // { id: 2, name: "Kl", description: "Hi from Lambda! ID# 2" },
    ]),
    //const message
    messafe = body["massafe"]
  };
  //return response;//let mes= event["hi"];
exports.handler = async (event, context, callback) => {
  // TODO implement
  console.log("----- lambda start")
  console.log(event);
 
   console.log("start if");
if(event.httpMethod === "post"){
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
    body:JSON.stringify({
      message:"succesfuly",
      details: body
    })
 };
 return response;
}
  callback(null, response);
};
