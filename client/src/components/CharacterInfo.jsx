
function CharacterInfo({selectedCharacter}) {
    const {character_name,hitpoints,mana,gold} = selectedCharacter || {};

    return(
        <div className="selected-character">
            {selectedCharacter ? (
                <>
                    <h2>{selectedCharacter.character_name}</h2>
                    <p>Gold:{gold}</p>
                    <img src='character1.png' alt='display-character'></img>
                    <p>{hitpoints}/MaxHitpoints</p>
                    <p>{mana}/MaxMana</p>
                </>
            ) : (
            <h2>No character selected</h2>
            )}
        </div>
    );
}
export default CharacterInfo;