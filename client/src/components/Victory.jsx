import {useOutletContext} from "react-router-dom";
import CharacterInfo from "./CharacterInfo";
function Victory() {
    const {selectedCharacter,navigate}= useOutletContext();
    return(
        <div className="victory-container">
            <h1 className="message-title">A Triumphant Victory</h1>
            <CharacterInfo selectedCharacter={selectedCharacter}/>
            <p className="message">Well Done, You feel yourself growing stronger and the jingle of coins in your purse grows more satisfying...</p>
            <div>
                <button className="message-button" onClick={()=>navigate('/town')}>Back to Town</button>
                <button className="message-button" onClick={()=>navigate('/battle')}>Keep Fighting</button>
            </div>
            
        </div>
    );
}
export default Victory;