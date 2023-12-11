import {useOutletContext} from "react-router-dom";
import { useFormik } from 'formik';
import * as yup from 'yup'
import {useState } from 'react';
import CharacterCard from "./CharacterCard";
import CharacterInfo from "./CharacterInfo";

function Home() {
    const [showCreate,setShowCreate] = useState(false)
    const {user,setSelectedCharacter, selectedCharacter}= useOutletContext();
    const charactersArray = user?.characters
    
    const handleCharacterClick = (character) => {
        fetch(`/character/${character.id}`)
        .then((r)=>{
            if (r.ok) {
                r.json().then((character)=> {
                    setSelectedCharacter(character);
                })
            }
        })
    }
    const renderCharacters = charactersArray?.map((character)=>(
        <CharacterCard
            key={character.id}
            character={character}
            handleClick={handleCharacterClick}
        />
    ))
    function handleButtonForm(){
        setShowCreate(!showCreate)
    }
    const signupSchema = yup.object().shape({
        character_name: yup.string().min(1,'Must Be?').max(50,'Less is better.'),
    })
    const formik = useFormik({
        initialValues: {
            character_name: '',
        },
        validationSchema: signupSchema,
        onSubmit: (values) => {
            fetch('/character',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values)
            }).then((r)=>{
                if (r.ok) {
                    r.json().then((character)=>{
                        setSelectedCharacter(character);
                        
                        //Navigate if i want
                    })
                } else {
                    console.log('errors')
                }
            })
        },
    });
    return(
        <section className="character-container">
            <div>
                <button onClick={handleButtonForm}>Create a new character</button>
                {showCreate && (
                <form onSubmit={formik.handleSubmit}>
                <div className='box-input'>
                    <input
                        type="text"
                        id="character_name"
                        name="character_name"
                        value={formik.values.character_name}
                        onChange={formik.handleChange}
                        required
                        placeholder=' '
                    />
                    <label htmlFor="character_name" >Character Name</label>
                </div>
                <button className='login-button' type="submit">Create</button>
                </form>
                )}
            </div>
            <div className="CC">
                <h2>Select a character</h2>
                <div className="character-list">{renderCharacters}</div>
            </div>
                <CharacterInfo selectedCharacter={selectedCharacter}/>
        </section>
    );
}
export default Home;