import { useLocation } from 'react-router-dom';
function CharacterInfo({selectedCharacter}) {
    const {character_name,hitpoints,max_hitpoints,mana,max_mana,gold,draw,id,decks,block,level,experience,experience_cap,skill_point} = selectedCharacter || {};
    const location = useLocation();
    return(
        <div className="selected-character">
            {selectedCharacter ? (
                <>
                    {location.pathname === '/' && <button className='Edit'>WIP Edit Character</button>}
                    <h2 className='Character-Title'>{character_name}</h2>
                    <div className="😭">
                        <p>Lv: {level}</p>
                    </div>
                    <img src='character1.png' alt='display-character'></img>
                    <div className="😭">
                        <p className="hp">{hitpoints}/{max_hitpoints} Hp</p>
                        <p className="mana">{mana}/{max_mana} Mana</p>
                    </div>
                    <div className="😭">
                        {location.pathname === '/battle' && <p>ManaRegen:10%</p>}
                        {location.pathname === '/battle' && <p className='block'>Blocking {block}</p>}
                    </div>
                    <div className="😭">
                        <p className="deck">{decks.length} Cards in Deck</p>
                        <p className='draw'>{draw} Draw</p>
                    </div>
                    <div className="😭">
                        <p className="deck">Gold:{gold}</p>
                        <p className='draw'>{experience}/{experience_cap} xp</p>
                    </div>
                    {skill_point > 0 && <p className="😭">{skill_point} skill point available</p>}
                </>
            ) : (
            <h2>No character selected</h2>
            )}
        </div>
    );
}
export default CharacterInfo;