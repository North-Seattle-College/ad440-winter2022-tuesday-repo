import React from "react";

function ClearButton({empty}) {

    return (
        <div>
            <button disabled={!empty} onClick="ClearButton({empty})">Clear</button>
        </div>    
    );    
}

export default ClearButton;