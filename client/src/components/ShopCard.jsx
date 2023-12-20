
import { useLocation } from 'react-router-dom';
function ShopCard({card,setSelectedCharacter,selectedCharacter,removeFromShowRolledShop}) {
    const location = useLocation();
    const {id,card_name,gold_cost,mana_cost,mana_gain,hp_cost,damage,block,heal,description,image} = card|| {};
    const formattedDescription = description
        .replace('{damage}', damage)
        .replace('{block}', block)
        .replace('{heal}', heal)
        .replace('{hp_cost}',hp_cost)
        .replace('{mana_gain}',mana_gain)
    const formattedDesc = formattedDescription.replace(/\n/g, '<br/>');
    const renderDescription = { __html: formattedDesc };

    const handleBuyCard = ()=> {
        if (selectedCharacter.gold >= gold_cost) {
            fetch(`/buycard/${id}`)
            .then((r)=>{
                if (r.ok) {
                    return r.json()
                } else {
                    throw new Error('Not Enough Gold');
                }
            }).then((data) => {
                setSelectedCharacter(data.character)
                removeFromShowRolledShop(id);
            }).catch((error) => {
                console.error(error);
            })
        } else {

        }
    }
    return(
        <span className="card" onClick={handleBuyCard}>
            <span className="😭">
                <h2 className="hp">{hp_cost} Hp</h2>
                <h2 className="mana">{mana_cost} Mana</h2>
            </span>
            <h1 >{card_name}</h1>
            {<img src={image} alt="Card Image" className="🤏"/>}
            <h3 dangerouslySetInnerHTML={renderDescription} />
            {location.pathname === '/town' && <p className='gold-cost'>{gold_cost} Gold</p>}
        </span>
    );
}
export default ShopCard;