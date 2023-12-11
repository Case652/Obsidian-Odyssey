


function Nav({handleLogout, user,selectedCharacter}) {
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
                    <li className="nav-li"><img className='nav-img' src='Settings.jpg' alt='settings'/><p className="nav-p">stuff added here</p></li>
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