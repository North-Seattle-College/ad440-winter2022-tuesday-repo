import React from "react";

export default function Feedback({response}) {
    return(
        <div className = "feedback">
            <br/>
            <strong>Analysis:</strong>
            <div className="analysis">{response}</div>
        </div>
    )

}