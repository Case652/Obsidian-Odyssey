import {useOutletContext} from "react-router-dom";
import CharacterInfo from "./CharacterInfo";
function Victory() {
    const {selectedCharacter,navigate}= useOutletContext();
    return(
        <div className="character-container">
            <h1 className="message-title">A Triumphant Victory</h1>
            <CharacterInfo selectedCharacter={selectedCharacter}/>
            <p className="message">Well Done, You feel yourself growning stronger and the jingle of coins in your purse grows more satisfying...</p>
            <button className="🥺" onClick={()=>navigate('/town')}>Back to Town</button>
        </div>
    );
}
export default Victory;