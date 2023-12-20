import {useOutletContext} from "react-router-dom";
import React, { useEffect} from "react";
function Defeat() {
    const {navigate,setUser}= useOutletContext();
    useEffect(() => {
        fetch('/authorized')
        .then((r) => {
            if (r.ok) {
                return r.json();
            } else if (r.status === 404) {
                navigate('/signup');
                throw new Error('User not found');
            } else {
                throw new Error('Unexpected In Auth');
            }
        })
        .then((user) => {
            setUser(user);
        })
        .catch((error) => console.error(error));
    }, [])
    return(
        <div className="defeat-container">
            <div>
                <h1 className="message-title">Defeat</h1>
                <p className="message">Well...I Suppose another poor soul will take up the cause</p>
                <button className="message-button" onClick={()=>navigate('/')}>Back to Character Selection</button>
            </div>
        </div>
    );
}
export default Defeat;