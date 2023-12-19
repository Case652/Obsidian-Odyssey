
function CharacterCard({character,handleClick}) {

    const {character_name,level} = character
    
    return(
        <span className="character-card" onClick={()=>handleClick(character)}>
            <h2>{character_name}</h2>
            <h2>Lv.{level}</h2>
        </span>
    );
}
export default CharacterCard;