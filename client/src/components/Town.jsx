import {useOutletContext} from "react-router-dom";

function Town() {
    const {setUser,user,setSelectedCharacter, selectedCharacter,navigate}= useOutletContext();
    return(
        <div className="character-container">
            In Town
        </div>
    );
}
export default Town;