import {useOutletContext} from "react-router-dom";
import { useFormik} from 'formik';
import * as yup from 'yup'
import {useState } from 'react';
import CharacterCard from "./CharacterCard";
import CharacterInfo from "./CharacterInfo";

function CharacterSelection() {
    const [showCreate,setShowCreate] = useState(false)
    const {setUser,user,setSelectedCharacter, selectedCharacter,navigate}= useOutletContext();
    const charactersArray = user?.characters
    const charactersPerRow = 4
    const rows = []

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
            setShowCreate(false)
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

    const renderCharacters = charactersArray?.map((character, index)=>(
        <CharacterCard
            key={character.id}
            character={character}
            handleClick={handleCharacterClick}
        />
    ))

    for (let i = 0; i <renderCharacters?.length; i += charactersPerRow){
        const rowCharacters = renderCharacters.slice(i, i + charactersPerRow);
        rows.push(rowCharacters)
    }
    const renderedCharacterGrid = rows.map((row,rowIndex)=>(
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

    function handleButtonForm(){
        setSelectedCharacter(null)
        setShowCreate(!showCreate)
    }

    const characterSchema = yup.object().shape({
        image: yup.string().required('Please select an image'),
        character_name: yup.string().min(1,'Must Be?').max(16,'Less is better.').required('Character name is required'),
    })

    const formik = useFormik({
        initialValues: {
            image: '',
            character_name: '',
        },
        validationSchema: characterSchema,
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
        const isConfirmed = window.confirm(`Are you sure?\n ${selectedCharacter.character_name}\n Will be deleted forever.`)

        if (isConfirmed) {
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
        } else {
            console.log('no character deleted.')
        }
    }
    const handleUnSelect = ()=> {
        setSelectedCharacter(null)
    }
    const imageOptions = [
        "/character/character1.png",
        "/character/character2.png",
        "/character/character3.png",
        "/character/character4.png",
        "/character/character5.png",
        "/character/character6.png",
        "/character/character7.png",
        "/character/character8.png",
        "/character/character9.png",
        "/character/character10.png",
        "/character/character11.png",
    ]
    return(
        <section className="character-container">
            {showCreate ? (
                <form className="selected-character" onSubmit={formik.handleSubmit}>
                    {formik.values.image ? (<img src={formik.values.image} alt="Preview" />) :(<img></img>)}
                    <div className='box-input'>
                        <select
                            id="image"
                            name="image"
                            onChange={formik.handleChange}
                            value={formik.values.image}
                            required
                        >
                        <option value="" disabled>Select an image</option>
                        {imageOptions.map((option) => (<option key={option} value={option}>{`Character Look ${imageOptions.indexOf(option) + 1}`}</option>))}
                        </select>
                        {formik.touched.image && formik.errors.image ? (<div className="error">{formik.errors.image}</div>) : null}
                    </div>
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
                        {formik.touched.character_name && formik.errors.character_name ? (<div className="error">{formik.errors.character_name}</div>) : null}
                    </div>
                    <button className='login-button' type="submit">Create</button>
                </form>
                ) : (
                <CharacterInfo selectedCharacter={selectedCharacter}/>
            )}
            <div className="😭">
                {selectedCharacter && (<button className="🥺" onClick={()=>navigate('/town')}>Go To Town</button>)}
                {showCreate ?(<button onClick={handleButtonForm} className="🥺">I've changed my mind</button>):(<button  className="🥺" onClick={handleButtonForm}>Create a new character</button>)}
                {selectedCharacter ? (<button className="🥺" onClick={handleDelete}>Delete Current Character</button>) :(<h2 className="🥺">Please Select A Character</h2>)}
                {selectedCharacter && (<button className="🥺" onClick={handleUnSelect}>Unselect Current Character</button>)}
            </div>
            <div className="slide-wrapper">
                <p className="slide-back" onClick={handleSlideBack}>Scroll Back</p>
                <div className="slide">
                    {renderedCharacterGrid}
                </div>
                <p className="slide-forward" onClick={handleSlideForward}>Scroll Forward</p>
            </div>
            
        </section>
    );
}
export default CharacterSelection;