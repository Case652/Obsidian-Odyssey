import {useOutletContext} from "react-router-dom";

function Defeat() {
    const {navigate}= useOutletContext();
    return(
        <div className="defeat-container">
            <div>
                <h1 className="message-title">Defeat</h1>
                <p className="message">Well...I Suppose another poor soul will take up the cause</p>
                <button className="message-button" onClick={()=>navigate('/')}>Back to Character Selection</button>
            </div>
        </div>
    );
}
export default Defeat;