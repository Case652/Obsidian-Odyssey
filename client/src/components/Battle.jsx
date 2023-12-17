import {useOutletContext} from "react-router-dom";
import Card from "./Card";
import CharacterInfo from "./CharacterInfo";
function Battle() {
    const {selectedCharacter} = useOutletContext();
    const cardsArray = selectedCharacter?.decks
    const cardsPerRow = 3
    const rows = []

    





    const renderCards = cardsArray?.map((cards, index)=>(
        <Card
            key={selectedCharacter.decks.id}
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

    return(
        <section className="character-container">
            <div className="😭">
                <div className="battle-left">
                    <CharacterInfo selectedCharacter={selectedCharacter}/>
                </div>
                <div className="battle-right">
                    <CharacterInfo selectedCharacter={selectedCharacter}/>
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