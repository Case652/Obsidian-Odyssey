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
  useEffect(()=>{
    fetch('/authorized').then((r)=>{
      if (r.ok) {
        r.json().then((user)=> setUser(user))
      } else if (r.status == 404){
        navigate('/signup');
      } else {
        throw new Error('Unexpected app.jsx.18')
      }
    }
    )
  },[])

  function handleLogout() {
    fetch('/logout',{
      method:'DELETE'
    }).then((r)=>{
      if (r.ok) {
        setUser(null)
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
  return <>
    <div className="App">
      <Nav handleLogout={handleLogout} user={user} selectedCharacter={selectedCharacter}/>
      <Outlet context={context}/>
    </div>
  </>
}

export default App;
