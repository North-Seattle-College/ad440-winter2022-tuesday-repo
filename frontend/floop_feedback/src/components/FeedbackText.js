import React from "react";
function FeedbackText ({feedback, setFeedback, setEmpty}) {
    return (
    <div>
      <div className="field">
        <label style={{fontSize:'20px'}}>Please enter a comment</label>
        <div>
          <textarea
            type ="text"
            value = {feedback}
            onChange={(e) => {
                if(e.target.value === ""){
                  setEmpty(false)
                  setFeedback("")
                }else{
                  setFeedback(e.target.value)
                  setEmpty(true)
              }
            }}
          />
        </div>
      </div>
    </div>
    );
  }
  export default FeedbackText;