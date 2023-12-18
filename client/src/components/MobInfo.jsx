
function MobInfo({ongoingFight}) {
    const {mob_name,hitpoints,max_hitpoints,mana,max_mana,draw,id,decks} = ongoingFight || {};
    return(
        <div className="selected-character">
            {ongoingFight ? (
                <>
                    <h2>{mob_name}</h2>
                    <img src='character1.png' alt='display-character'></img>
                    <div className="😭">
                        <p className="hp">{hitpoints}/{max_hitpoints} Hp</p>
                        <p className="mana">{mana}/{max_mana} Mana</p>
                    </div>
                    <p>{draw} Draw</p>
                </>
            ) : (
            <h2>No character selected</h2>
            )}
        </div>
    );
}
export default MobInfo;