
function Nav({handleLogout, user,selectedCharacter,navigate}) {
    const {character_name} = selectedCharacter || {};

    return(
            <div className="navbar">
                <div className="nav-user">
                    <img src='logo512.png' alt='User Avatar' className='nav-user-img'/>
                    <div>
                        <h2>{user?.username}</h2>
                        <p>{character_name}</p>
                    </div>
                </div>
                <ul className="nav-ul">
                    {user && <li className="nav-li" onClick={()=>navigate('/')}><img className='nav-img' src='Settings.jpg' alt='settings' /><p className="nav-p">Character Selection</p></li>}
                    {selectedCharacter &&<li className="nav-li" onClick={()=>navigate('/battle')}><img className='nav-img' src='Settings.jpg' alt='settings' /><p className="nav-p">Battle</p></li>}
                    {selectedCharacter &&<li className="nav-li" onClick={()=>navigate('/town')}><img className='nav-img' src='Settings.jpg' alt='settings' /><p className="nav-p">Town</p></li>}
                    <li className="nav-li"><img className='nav-img' src='logo192.png' alt='links png'/><p className="nav-p">stuff added here</p></li>
                    
                </ul>
                {user && (
                    <ul className="nav-ul" onClick={handleLogout}>
                        <li className="nav-li"><img className='nav-img' src='Logout.jpg' alt='Logout Png'/><p className="nav-p">Logout</p></li>
                    </ul>
                )}
            </div>
    );
}
export default Nav;