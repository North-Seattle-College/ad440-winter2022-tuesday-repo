import React from "react";

function SubmitButton({empty, feedback, setResponse, setError}) {
  const inputSubmit = e => {
    const requestConfig = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
    };
    e.preventDefault();
    fetch('https://d5z72uewg7.execute-api.us-west-2.amazonaws.com/feedback/kj-6exxg-20220222-lambda', requestConfig)
      .then(response => {
        if(!response.ok) {
        }
        return response.json();
      })
      .then(data => {
        setResponse(data);
      })
      .catch(err => { setError(err) });
  }
  return (
    <div>
      <button disabled={!empty} onClick={inputSubmit}>Submit</button>
    </div>
  );
}

export default SubmitButton;
