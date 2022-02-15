import React, { useState } from 'react'

import FeedbackText from './FeedbackText';
import FeedbackAnalysis from './FeedbackAnalysis';
import SubmitButton from './SubmitButton';
import ErrorMessage from './ErrorMessage';

const Container = () => {
    const [feedback, setFeedback] = useState('');
    const [response, setResponse] = useState('');
    const [empty, setEmpty] = useState(false);
    const [error, setError] = useState(false);
    
    return (
        <div className="ui card" style={{margin:'50px'}}>
            <FeedbackText feedback={feedback} setFeedback={setFeedback} setEmpty={setEmpty} />
            <SubmitButton empty={empty} feedback={feedback} setResponse={setResponse} setError={setError} />
            {!error ? <FeedbackAnalysis response={response} /> : <ErrorMessage error={Error}/>}
        </div>
    );
}

export default Container;
