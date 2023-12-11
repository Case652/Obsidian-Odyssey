import {useOutletContext} from "react-router-dom";
import { useFormik } from 'formik';
import * as yup from 'yup'
import {useState } from 'react';
import CharacterCard from "./CharacterCard";
import CharacterInfo from "./CharacterInfo";

function Home() {
    const [showCreate,setShowCreate] = useState(false)
    const {setUser,user,setSelectedCharacter, selectedCharacter}= useOutletContext();
    const charactersArray = user?.characters
    
    const handleCharacterClick = (character) => {
        fetch(`/character/${character.id}`)
        .then((r) => {
            if (r.ok) {
                return r.json();
            } else {
                throw new Error('Failed to fetch character');
            }
        })
        .then((character) => {
            setSelectedCharacter(character);
            fetch(`/changeChar`,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                }, body: JSON.stringify({character_id:character.id}),
            })
            .then((r) => {
                if (!r.ok) {
                throw new Error('Failed to set session character_id');
                }
            })
            .catch((error) => console.error(error));
        })
        .catch((error) => console.error(error));
    };
    
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
                        setUser((prevUser) => {
                            return {
                                ...prevUser,
                                characters: [...prevUser.characters, character],
                            };
                        });
                        setSelectedCharacter(character);
                        setShowCreate(!showCreate)
                        //Navigate if i want
                    })
                } else {
                    console.log('errors')
                }
            })
        },
    });
    const handleDelete = ()=>{
        fetch(`/character/${selectedCharacter.id}`,{
            method:'DELETE',
            headers:{
                'Content-Type':'application/json'
            },
        }).then((r)=>{
            if (r.ok) {
                setUser((prevUser) => {
                    const updatedCharacters = prevUser.characters.filter((character) => character.id !== selectedCharacter.id);
                    return {
                        ...prevUser,
                        characters: updatedCharacters,
                    };
                });
                setSelectedCharacter(null)
                console.log('deleted')
            } else {
                console.log('failed to delete')
            }
        })
    }
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
                <CharacterInfo selectedCharacter={selectedCharacter} handleDelete={handleDelete}/>
        </section>
    );
}
export default Home;