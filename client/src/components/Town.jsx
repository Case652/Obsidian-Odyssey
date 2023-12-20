import {useOutletContext} from "react-router-dom";
import { useState} from 'react';
import Card from "./Card";
import ShopCard from "./ShopCard"
import CharacterInfo from "./CharacterInfo";
function Town() {
    const {selectedCharacter,setSelectedCharacter,navigate,setOngoingFight} = useOutletContext();
    const [showCards, setShowCards] = useState(true);
    const [showShop,setShowShop] = useState(false);
    const [showRolledShop,setShowRolledShop] = useState(null);
    const [activeFilter, setActiveFilter] = useState('ShowDeck');
    const [leveling,setLeveling] = useState(false)
    const cardsArray = selectedCharacter?.decks
    const removeFromShowRolledShop = (cardIdToRemove) => {
        setShowRolledShop((prevRolledShop) =>
            prevRolledShop.filter((card) => card.id !== cardIdToRemove)
        );
    };
    const renderCards = cardsArray?.map((card)=>(
        showCards && (
            <Card
                key={card.id}
                card={card}
                setSelectedCharacter={setSelectedCharacter}
                setOngoingFight={setOngoingFight}
            />
        )
    ))
    const renderShop = showRolledShop?.map((card)=>(
        showShop && (
            <ShopCard
                key={card.id}
                card={card}
                setSelectedCharacter={setSelectedCharacter}
                selectedCharacter={selectedCharacter}
                removeFromShowRolledShop={removeFromShowRolledShop}
            />
        )
    ))
    const handleShowDeck=()=>{
        setActiveFilter(activeFilter === 'ShowDeck' ? null : 'ShowDeck');
        setShowCards(!showCards)
        setShowShop(false)
    }
    const handleToggleSkillPoints = () => {
        setLeveling(!leveling)
    };
    const handleShowShopText=()=>{
        setActiveFilter(activeFilter === 'ShowShop' ? null : 'ShowShop');
        setShowShop(!showShop)
        setShowCards(false)
    }
    const handleShopRoll100=()=>{
        if (selectedCharacter.gold >= 100){
            fetch('/shop100')
            .then((r)=>{
                if (r.ok) {
                    return r.json()
                    
                } else {
                    throw new Error('Not Enough Gold');
                }
            }).then((data) => {
                setSelectedCharacter(data.character)
                setShowRolledShop(data.available_cards)
            }).catch((error) => {
                console.error(error);
            })
        }
    }
    const handleShopRoll300=()=>{
        if (selectedCharacter.gold >= 300){
            fetch('/shop300')
            .then((r)=>{
                if (r.ok) {
                    return r.json()
                    
                } else {
                    throw new Error('Not Enough Gold');
                }
            }).then((data) => {
                setSelectedCharacter(data.character)
                setShowRolledShop(data.available_cards)
            }).catch((error) => {
                console.error(error);
            })
        }
    }
    return(
        <div className="town-container">
            <div className="stack">
                <CharacterInfo selectedCharacter={selectedCharacter}/>
                
                {leveling ? (<div className="panel">
                    <>Spend Your Skills Here!</>
                    <button>1 Point For 10 extra Max Hitpoints(WIP)</button>
                    <button>1 Point For 10 extra Max Mana(WIP)</button>
                    <button>5 Point For 1 extra Draw(WIP)</button>
                    <button className="🎮" onClick={handleToggleSkillPoints}>Maybe Later</button>
                </div>
                ):(<div className="panel">
                    <>Welcome to Town, You can buy cards</>
                    <div className="😭">
                        <button className={`🎮 ${activeFilter === 'ShowDeck' ? '🎮🎮' : ''}`} onClick={handleShowDeck}>ShowDeck</button>
                        <button className={`🎮 ${activeFilter === 'ShowShop' ? '🎮🎮' : ''}`} onClick={handleShowShopText}>ShowShop</button>
                    </div>
                    <button className="🎮" onClick={handleToggleSkillPoints}>Spend SkillPoints</button>
                    <button onClick={()=>navigate('/battle')} className="🎮" >Earn Some Gold Fighting</button>
                </div>)}
            </div>

            {showRolledShop === null ? (<div className="cards-container">
                {showShop &&<p className="message">You stop by a shady stall...</p>}
                {showShop &&<p className="message">A thin figure speaks:</p>}
                {showShop &&<p className="message">"For a mere handful of gold, you could possess mysterious and rare cards I've acquired from the deepest corners of the realms "</p>}
                {showShop &&<p></p>}
                {showShop &&<p className="message">*The audacity to demand payment for merely glimpsing what they peddle. *</p>}
                {showShop &&<p></p>}
                {showShop &&<button className="🥺" onClick={handleShowShopText}>Walk away</button>}
                {showShop &&<button className="🥺" onClick={handleShopRoll100}>Slip him 100 gold</button>}
                {showShop &&<button className="🥺" onClick={handleShopRoll300}> Chuck 300 gold at him</button>}

                {renderCards}
            </div>) : (
                <div className="cards-container">
                    
                    {showRolledShop && showShop && (<button className="🥺" onClick={handleShopRoll100}>Slip him another 100 gold </button>)}
                    {showRolledShop && showShop && (<button className="🥺" onClick={handleShopRoll300}> Waste 300 gold</button>)}
                    {showRolledShop && showShop &&<button className="🥺" onClick={handleShowShopText}>Walk away</button>}
                    {renderShop}
                    {renderCards}
                </div>
            )}
        </div>
    );
}
export default Town;