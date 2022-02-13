import React from "react";

const Feedback = (props) =>{
    return(
        <div style={{overflowWrap:"break-word"}}>
             {props.content.message}
        </div>
    );
};

export default Feedback;