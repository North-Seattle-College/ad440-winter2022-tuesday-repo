import React from "react";

export default function FeedbackAnalysis({response}) {
    return(
        <div className = "feedback">
            <br/>
            <div className="analysis">{response}</div>
        </div>
    )
}