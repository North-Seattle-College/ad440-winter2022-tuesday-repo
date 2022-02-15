import React from "react";

function SubmitButton({empty, feedback, setResponse, setError}) {
  const inputSubmit = e => {
    const requestConfig = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback })
    };
    e.preventDefault();
    fetch('https://9u4xt4nqr1.execute-api.us-west-2.amazonaws.com/default/test', requestConfig)
      .then(response => {
        if(!response.ok) {
          setError('Network response not ok');
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
