import React from "react";

function ClearButton({empty}) {

    return (
        <div>
            <button disabled={!empty} onClick={<a href="/"/>}>Clear</button>
        </div>    
    );    
}

export default ClearButton;