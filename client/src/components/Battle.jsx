import { useState, useEffect } from 'react';
import {useOutletContext} from "react-router-dom";
import Card from "./Card";
import MobInfo from './MobInfo';
import CharacterInfo from "./CharacterInfo";
function Battle() {
    const {selectedCharacter,setSelectedCharacter} = useOutletContext();
    const [ongoingFight, setOngoingFight] = useState(null);
    const cardsArray = selectedCharacter?.decks
    const cardsPerRow = 3
    const rows = []
    const renderCards = cardsArray?.filter((card) => card.status === 'Drawn').map((card, index)=>(
        <Card
            key={card.id}
            card={card}
            setSelectedCharacter={setSelectedCharacter}
            setOngoingFight={setOngoingFight}
        />
    ))

    for (let i = 0; i <renderCards?.length; i += cardsPerRow){
        const rowCards = renderCards.slice(i, i + cardsPerRow);
        rows.push(rowCards)
    }
    const renderedCardGrid = rows.map((row,rowIndex)=>(
        <div key={rowIndex}>{row}</div>
    ))
    
    const handleSlideBack = () => {
        const slide = document.querySelector('.slide');
        slide.style.scrollBehavior = 'smooth'
        slide.scrollLeft -= 900
    }

    const handleSlideForward = () => {
        const slide = document.querySelector('.slide');
        slide.style.scrollBehavior = 'smooth'
        slide.scrollLeft += 900
    }

    useEffect(()=>{
        if (selectedCharacter && selectedCharacter.id) {
            fetch(`/fight/${selectedCharacter.id}`)
            .then((r)=>{
                if (r.ok) {
                    console.log('Fight is ongoing')
                    return r.json();
                } else if (r.status === 201) {
                    console.log('Created a new fight')
                    return r.json();
                } else if(r.status === 404) {
                    console.log('Character not found')
                    return null;
                } else {
                    throw new Error('Somthing is unexpected wrong')
                }
            }).then((fight)=>{
                console.log(fight.character)
                if (fight !== null) {
                    setSelectedCharacter(fight.character)
                    setOngoingFight(fight);
                }
            }).catch((error) =>{
                console.error('error fetching fight',error)
            })
        }
    },[selectedCharacter?.id])
    const handleEndTurn=()=>{
        console.log("fetch to end turn")
    }
    return(
        <section className="character-container">
            <div className="😭">
                <div className="battle-left">
                    <CharacterInfo selectedCharacter={selectedCharacter}/>
                </div>
                <div className="battle-right">
                    <MobInfo ongoingFight={ongoingFight}/>
                </div>
            </div>
            <div className="slide-wrapper">
                <p className="slide-back" onClick={handleSlideBack}>Scroll Back</p>
                <div className="slide">
                    {renderedCardGrid}
                </div>
                <p className="slide-forward" onClick={handleSlideForward}>Scroll Forward</p>
            </div>
        </section>
    );
}
export default Battle;