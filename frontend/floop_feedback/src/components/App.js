import React from "react";
import InputTextBar from "./InputTextBar";
import Feedback from "./Feedback";
import Container from "./Container";

class App extends React.Component{
    // state = { content: ''}
    // onInputSubmit = term => {
    //     // API here maybe?
    //     console.log(term);
    //     this.setState({content: term})
    // }
    render(){
        return (
            <Container />
            // <div className="ui card" style={{margin:'50px'}}>
            //     <InputTextBar onSubmit={this.onInputSubmit} />
            //     <Feedback content = {this.state.content} />
            // </div>
        );
    }
}

export default App;