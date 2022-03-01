import React from "react";
function FeedbackText ({feedback, setFeedback, setEmpty}) {
    return (
    <div>
      <div className="field">
        <label>Please provide your feedback</label>
        <div>
          <textarea
            type ="text"
            placeholder="Type your message here"
            value = {feedback}
            onChange={(e) => {
                if(e.target.value === ""){
                  setEmpty(false)
                  setFeedback("")
                }else{
                  setFeedback(e.target.value)
                  setEmpty(true)
              }
              console.log(feedback)
            }}
          />
        </div>
      </div>
    </div>
    );
  }
  export default FeedbackText;