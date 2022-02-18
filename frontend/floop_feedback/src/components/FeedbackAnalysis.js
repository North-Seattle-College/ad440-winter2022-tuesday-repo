import React from "react";

export default function FeedbackAnalysis({response}) {
    return(
        <div className = "feedback">
            <br/>
            <strong>Analysis:</strong>
            <div className="analysis">{response}</div>
        </div>
    )
}