# POST Prototype for React app

## This is a prototype to send a POST request

### We send the feedback and recieve a response of the feedback insight

---

- Based off of Jia's component App, from this [PR](https://github.com/North-Seattle-College/ad440-winter2022-tuesday-repo/pull/26).
- This references the backend's swagger document from this [PR](https://github.com/North-Seattle-College/ad440-winter2022-tuesday-repo/pull/20)
- Uses fetch to handle requests, as this is what the current Floop app uses.
- The only error handeling is a console.log statement if the fetch statement catches an error. This will need to be updated.
- This is an **untested** example of a POST request.
- I would replace line 6 `state = { content: ''}` with `const [content, setContent] = useState('')` and utilize React's useState and hooks
- This requires the correct url for the api request

---

When using fetch() for an API request, make sure the request body is the correct content-type that is in the header. The response is a promise and you can call various methods on this to parse it in different formats. I used JSON below for the request and text for the response. The text for the response is based off of Jia's current component. We may want to handle this as JSON.

Fetch returns a response object that has a Boolean 'ok', a status (ex: 400), the status text, and the response. Both the status and the ok can be used for error handeling.

---

```
import React, { useState } from 'react';

const [content, setContent] = useState('');

const onInputSubmit = (term) => {
  const requestConfig = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: term })
  };

  fetch("https://floop.com/api/assignment/${props.id}", requestConfig)
    .then(response => response.text())
    .then(content => { setContent(content); })
    .catch(err => console.log('Unknown error: ', err));
};
```

---

References

https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

https://javascript.info/fetch

https://www.javascripttutorial.net/javascript-fetch-api/
