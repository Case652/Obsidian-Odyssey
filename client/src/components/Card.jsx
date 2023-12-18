
function Card({card}) {
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