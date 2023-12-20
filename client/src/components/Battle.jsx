import { useState, useEffect } from 'react';
import {useOutletContext} from "react-router-dom";
import Card from "./Card";
import MobInfo from './MobInfo';
import CharacterInfo from "./CharacterInfo";
function Battle() {
    const {selectedCharacter,setSelectedCharacter,navigate} = useOutletContext();
    const [ongoingFight, setOngoingFight] = useState(null);
    const [activeFilter, setActiveFilter] = useState('Drawn');
    const cardsArray = selectedCharacter?.decks
    const cardsPerRow = 3
    const rows = []
    const [filterType, setFilterType] = useState('Drawn');
    const filteredCards = cardsArray?.filter((card) => {
        switch (filterType) {
            case 'All':
                return true;
            case 'Drawn':
                return card.status === 'Drawn';
            case 'Undrawn':
                return card.status === 'Undrawn';
            case 'Discarded':
                return card.status === 'Discarded';
            case 'Exhausted':
                return card.status === 'Exhausted';
            default:
                return true;
        }
    });

    const renderCards = filteredCards?.map((card, index)=>(
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
        console.log("ending turn")
        fetch(`/endturn/${ongoingFight.id}`)
        .then((r)=>{
            if (r.ok) {
                console.log('turn ended and a new one has started')
                return r.json();
            } else if (r.status === 418){
                setSelectedCharacter(null)
                navigate('/defeat')
            } else {
                throw new Error('Somthing is unexpected wrong')
            }
        }).then((fight)=>{
            if (fight !== null) {
                setSelectedCharacter(fight.character)
                setOngoingFight(fight);
            }
        }).catch((error) =>{
            console.error('error fetching fight',error)
        })
    }
    const handleFilter = (filterType) => {
        setFilterType(filterType);
        setActiveFilter(filterType);
    };
    const handleFlee=()=>{
        fetch('/flee')
        .then((r)=>{
            if (r.ok){
                setOngoingFight(null)
                navigate('/town')
            } else {throw new Error('Somthing is unexpected wrong')}
        }).catch((error) =>{
            console.error('error fetching fight',error)
        })
    }
    return(
        <section className="battle-container">
            <div className="😭">
                <div className="battle-left">
                    <CharacterInfo selectedCharacter={selectedCharacter}/>
                    <button className={`💨 ${activeFilter === 'All' ? '💨💨' : ''}`}onClick={() => handleFilter('All')}>All Cards</button>
                    <button className={`💨 ${activeFilter === 'Drawn' ? '💨💨' : ''}`}onClick={() => handleFilter('Drawn')}>Drawn</button>
                    <button className={`💨 ${activeFilter === 'Undrawn' ? '💨💨' : ''}`}onClick={() => handleFilter('Undrawn')}>Undrawn</button>
                    <button className={`💨 ${activeFilter === 'Discarded' ? '💨💨' : ''}`}onClick={() => handleFilter('Discarded')}>Discarded</button>
                    <button className={`💨 ${activeFilter === 'Exhausted' ? '💨💨' : ''}`}onClick={() => handleFilter('Exhausted')}>Exhausted</button>
                </div>
                <div className="battle-right">
                    <MobInfo ongoingFight={ongoingFight}/>
                    <button className={`💨`} onClick={handleEndTurn}>End Turn</button>
                    <button className={`💨`} onClick={handleFlee}>Run-Away</button>
                    {/* <button className={`💨`}>SwitchView(WIP)</button> */}
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