import React from "react";
import LogoText from "../components/images/Floop_Logo_Text.png"

function Header() {
    return (
        <div>
            <a href="/"><img src={LogoText} alt="Floop Logo with Text" className="Logo_Text"/></a>
        </div>    
    );    
}

export default Header;