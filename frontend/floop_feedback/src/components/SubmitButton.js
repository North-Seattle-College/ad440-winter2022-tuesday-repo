import React from "react";

function SubmitButton({empty, feedback, setResponse, setError}) {
  const inputSubmit = e => {
    const requestConfig = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
      mode: 'no-cors'
    };
    e.preventDefault();
    fetch('https://d5z72uewg7.execute-api.us-west-2.amazonaws.com/test/kj-6exxg-20220222-lambda', requestConfig)
      .then(response => {
        console.log(response);
        if(!response.ok) {
          setError('Network response not ok');
        }
        return response.json();
      })
      .then(data => {
        setResponse(data);
      })
      .catch(err => { setError(err) });
      console.log(feedback, requestConfig, typeof feedback);
  }
  return (
    <div>
      <button disabled={!empty} onClick={inputSubmit}>Submit</button>
    </div>
  );
}

export default SubmitButton;
