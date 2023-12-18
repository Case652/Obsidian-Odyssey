
function Card({card,setOngoingFight,setSelectedCharacter}) {
    const {id,card_name,gold_cost,mana_cost,mana_gain,hp_cost,damage,block,heal,description} = card.card || {};
    console.log(card.card)
    const formattedDescription = description
        .replace('{damage}', damage)
        .replace('{block}', block)
        .replace('{heal}', heal)
        .replace('{hp_cost}',hp_cost)
        .replace('{mana_gain}',mana_gain)
    const formattedDesc = formattedDescription.replace(/\n/g, '<br/>');
    const renderDescription = { __html: formattedDesc };
    const handlePlayCard = ()=> {
        fetch(`/PlayCard/${id}`)
        .then((r)=>{
            if (r.ok){
            return r.json();
            } else {throw new Error('Somthing is unexpected wrong')}
        }).then((fight)=>{
            if (fight !== null) {
                setSelectedCharacter(fight.character)
                setOngoingFight(fight);
            }
        }).catch((error) =>{
            console.error('error fetching fight',error)
        })
    }
    return(
        <span className="card" onClick={handlePlayCard}>
            <span className="😭">
                <h2 className="hp">{hp_cost} hp</h2>
                <h2 className="mana">{mana_cost} mana</h2>
            </span>
            
            <h1 >{card_name}</h1>
            {/* Divs Interact weird & add a image*/}
            <h3 dangerouslySetInnerHTML={renderDescription} />
            {/* Goldcost bottem corner rightside for shop expansion*/}
        </span>
    );
}
export default Card;