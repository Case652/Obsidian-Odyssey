
function CharacterCard({character,handleClick}) {
    const {character_name} = character
    return(
        <div className="character-card" onClick={()=>handleClick(character)}>
            <h2>{character_name}</h2>
        </div>
    );
}
export default CharacterCard;