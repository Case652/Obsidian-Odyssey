import { useLocation } from 'react-router-dom';
function CharacterInfo({selectedCharacter}) {
    const {character_name,hitpoints,max_hitpoints,mana,max_mana,gold,draw,id,decks,block} = selectedCharacter || {};
    const location = useLocation();
    return(
        <div className="selected-character">
            {selectedCharacter ? (
                <>
                    <h2>{character_name}</h2>
                    <p>Gold:{gold}</p>
                    <img src='character1.png' alt='display-character'></img>
                    <div className="😭">
                        <p className="hp">{hitpoints}/{max_hitpoints} Hp</p>
                        <p className="mana">{mana}/{max_mana} Mana</p>
                    </div>
                    <div className="😭">
                        {location.pathname === '/battle' && <p>Blocking {block}</p>}
                        {location.pathname === '/battle' && <p className='block'>Blocking {block}</p>}
                    </div>
                    <p>{decks.length} Cards in Deck</p>
                    <p>{draw} Draw</p>
                </>
            ) : (
            <h2>No character selected</h2>
            )}
        </div>
    );
}
export default CharacterInfo;