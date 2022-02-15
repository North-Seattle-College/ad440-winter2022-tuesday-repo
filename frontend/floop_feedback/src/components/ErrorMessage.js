import React from 'react';
import ReactDOM from 'react-dom';
//import InputTextBar from "./InputTextBar";

function ErrorMessage() {
  const [errorMessage, setErrorMessage] = React.useState("");
  const handleClick = () => {
    setErrorMessage("Example error message!")
  }
  return (
    <div className="ErrorMessage">
      <button onClick={handleClick}>Show error message</button>
      {errorMessage && <div className="error"> {errorMessage} </div>}
    </div>
  );
}

ReactDOM.render(
  <ErrorMessage />, 
  document.getElementById('root')
);

export default ErrorMessage;