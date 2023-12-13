import React, { useEffect, useState } from "react";
import { Navigate, Outlet,useNavigate } from 'react-router-dom';
// import { Switch, Route } from "react-router-dom";

import Signup from "./Signup";
import Nav from './Nav'
function App() {
  const navigate = useNavigate();
  const [user,setUser] = useState(null)
  const [signup,setSignup] = useState(false)
  const [selectedCharacter, setSelectedCharacter] = useState(null);
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
        if (user) {
          fetch('/authCharacter')
            .then((r) => {
              if (r.ok) {
                return r.json();
              } else {
                throw new Error('Unexpected In AuthChar');
              }
            })
            .then((character) => setSelectedCharacter(character))
            .catch((error) => console.error(error));
        }
      })
      .catch((error) => console.error(error));
  }, [])
  function handleLogout() {
    fetch('/logout',{
      method:'DELETE'
    }).then((r)=>{
      if (r.ok) {
        setUser(null)
        setSelectedCharacter(null)
        navigate('/signup')
      }
    })
  }
  const context = {
    setSignup,
    signup,
    setUser,
    user,
    navigate,
    selectedCharacter,
    setSelectedCharacter,
  }
  return (
    <div className="App">
      <Nav handleLogout={handleLogout} user={user} selectedCharacter={selectedCharacter} navigate={navigate}/>
      <Outlet context={context}/>
    </div>
  )
}

export default App;
