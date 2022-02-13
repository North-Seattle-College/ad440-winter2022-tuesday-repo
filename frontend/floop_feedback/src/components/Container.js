import React, { useState } from 'react'

import Feedback from './Feedback';
import InputTextBar from './InputTextBar';

const Container = () => {

    const [state, setState] = useState('')
    const [content, setContent] = useState('')
    const [isVisible, setIsVisible] = useState(false)

    const onInputSubmit = term => {
        const requestConfig = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: term })
        };

        fetch("https://reqres.in/api/users/", requestConfig)
          .then(res => {
                return res.json()
          })
          .then(content => { setContent(content); })
          .catch(err => console.log('Unknown error: ', err));

          console.log(term);

          setState({content: term})
    }
    
    return (
        <div className="ui card" style={{margin:'50px'}}>
            <InputTextBar onSubmit={onInputSubmit} />
            <Feedback content = {content} />
            {/* {isVisible? <ErrorMessage /> : null} */}
        </div>
    )
}

export default Container;