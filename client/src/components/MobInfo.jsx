import MobCard from "./MobCard";
function MobInfo({ongoingFight}) {
    const {mob_name,hitpoints,max_hitpoints,mana,max_mana,draw,id,in_fight_mob_decks,block} = ongoingFight || {};
    const mobCards = in_fight_mob_decks || [];
    const renderMobCards = mobCards?.filter((card) => card.status === "Drawn").map((card)=>(
        <MobCard
            key={card.id}
            card={card}
        />
    ))
    return(
        <div className="selected-character">
            {ongoingFight ? (
                <>
                    <h2 className="Character-Title">{mob_name}</h2>
                    <img src='character1.png' alt='display-character'></img>
                    <div className="😭">
                        <p className="hp">{hitpoints}/{max_hitpoints} Hp</p>
                        <p className="block">Blocking {block}</p>
                    </div>
                    <div className="😭">{renderMobCards}</div>
                    
                </>
            ) : (
            <>
                <h2>No Fight In Progress...</h2>
                <h2>Please Wait A Moment...</h2>
            </>
            )}
        </div>
    );
}
export default MobInfo;