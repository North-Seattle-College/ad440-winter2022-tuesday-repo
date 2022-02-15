import React from 'react';

function ErrorMessage ({error}) {
  return (
    <div className="ErrorMessage ui">
      <textarea readOnly
        value = {error}
      />
    </div>
  );
}

export default ErrorMessage;