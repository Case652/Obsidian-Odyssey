
function CharacterInfo({selectedCharacter,handleDelete}) {
    const {character_name,hitpoints,mana,gold,id} = selectedCharacter || {};
    return(
        <div className="selected-character">
            {selectedCharacter ? (
                <>
                    <h2>{character_name}</h2>
                    <p>Gold:{gold}</p>
                    <img src='character1.png' alt='display-character'></img>
                    <p>{hitpoints}/MaxHitpoints</p>
                    <p>{mana}/MaxMana</p>
                    <button onClick={handleDelete}>Delete Character</button>
                </>
            ) : (
            <h2>No character selected</h2>
            )}
        </div>
    );
}
export default CharacterInfo;