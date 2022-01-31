import React from "react";

const Feedback = (props) =>{
    return(
        <div style={{overflowWrap:"break-word"}}>
             {props.content}
        </div>
    );
};

export default Feedback;