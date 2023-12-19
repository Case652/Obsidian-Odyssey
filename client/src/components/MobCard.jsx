
function MobCard({card}) {
    const {id,card_name,mana_gain,hp_cost,damage,block,heal,description} = card.card || {};
    const formattedDescription = description
        .replace('{damage}', damage)
        .replace('{block}', block)
        .replace('{heal}', heal)
        .replace('{hp_cost}',hp_cost)
        .replace('{mana_gain}',mana_gain)
    const formattedDesc = formattedDescription.replace(/\n/g, '<br/>');
    const renderDescription = { __html: formattedDesc };

    return(
        <span className="mob-card">
            <h1 >{card_name}</h1>
            <h3 dangerouslySetInnerHTML={renderDescription} />
        </span>
    );
}
export default MobCard;