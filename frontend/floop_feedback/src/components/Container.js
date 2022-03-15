import React, { useState } from 'react'

import FeedbackText from './FeedbackText';
import FeedbackAnalysis from './FeedbackAnalysis';
import SubmitButton from './SubmitButton';
import ClearButton from './ClearButton';
import ErrorMessage from './ErrorMessage';
import Header from './Header';
import Footer from './Footer';
import '../components/styles/Container.css'

const Container = () => {
    const [feedback, setFeedback] = useState('');
    const [response, setResponse] = useState('');
    const [empty, setEmpty] = useState(false);
    const [error, setError] = useState(false);
    
    return (
        <div className="App">
            <div className='Header'>
                <Header/>
            </div>
            <form>
                <div className='FeedbackText'>
                    <FeedbackText feedback={feedback} setFeedback={setFeedback} setEmpty={setEmpty} />
                </div>
                <div className='Button'>
                    <SubmitButton empty={empty} feedback={feedback} setResponse={setResponse} setError={setError} />
                    <ClearButton empty={empty} />
                </div>    
                <div className='Analysis'>
                    {!error ? <FeedbackAnalysis response={response.body} /> : <ErrorMessage error={error}/>}
                </div>
            </form>
            <div className='Footer'>
                <Footer/>
            </div>    
        </div>
    );
}

export default Container;
