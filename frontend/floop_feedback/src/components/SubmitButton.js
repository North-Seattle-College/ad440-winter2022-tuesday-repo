import React from "react";

function SubmitButton({empty, feedback, setResponse, setError}) {
  const url = 'https://api.holodium.com/v1/feedback'
  const inputSubmit = e => {
    const requestConfig = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
    };
    e.preventDefault();
    fetch(url, requestConfig)
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
