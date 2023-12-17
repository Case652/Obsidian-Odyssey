
function CharacterCard({character,handleClick}) {

    const {character_name} = character
    
    return(
        <span className="character-card" onClick={()=>handleClick(character)}>
            <h2>{character_name}</h2>
            <h2>Lv?</h2>
        </span>
    );
}
export default CharacterCard;