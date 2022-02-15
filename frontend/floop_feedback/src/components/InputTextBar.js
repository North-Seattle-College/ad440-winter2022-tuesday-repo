import React from "react";
import ErrorMessage from "./ErrorMessage";

class InputTextBar extends React.Component {
    state = {term: ''};

    onFormSubmit = event => {
        event.preventDefault();

        this.props.onSubmit(this.state.term);
    };

    render(){
        return (
        <div>
            <form onSubmit = {this.onFormSubmit} className="ui form">
                <div className="field">
                    <label style={{fontSize:'20px'}}>Please enter a comment</label>
                    <textarea
                        type ="text"
                        value = {this.state.term}
                        onChange={(e) => this.setState({term: e.target.value})}/>
                </div>
                <div className="ui button" style={{marginLeft:'190px', marginBottom:"5px"}} onClick={this.onFormSubmit}>
                    Submit
                </div>
                <ErrorMessage onSubmit={this.onInputSubmit} />
            </form>
        </div>
        );
    }
}

export default InputTextBar