import { useLocation } from 'react-router-dom';
function Nav({handleLogout, user,selectedCharacter,navigate}) {
    const location = useLocation();
    const {character_name} = selectedCharacter || {};
    return(
            <div className="navbar">
                <div className="nav-user">
                    <img src='/Icons/Logo.png' alt='User Avatar' className='nav-user-img'/>
                    <div>
                        <h2>{user?.username}</h2>
                        <p>{character_name}</p>
                    </div>
                </div>
                <ul className="nav-ul">
                    {(location.pathname === '/battle') ||user && <li className="nav-li" onClick={()=>navigate('/')}><img className='nav-img' src='/Icons/town.png' alt='settings' /><p className="nav-p">Character Selection</p></li>}
                    {(location.pathname === '/battle') ||selectedCharacter && <li className="nav-li" onClick={()=>navigate('/battle')}><img className='nav-img' src='/Icons/Battle.png' alt='settings' /><p className="nav-p">Battle</p></li>}
                    {(location.pathname === '/battle') || (location.pathname === '/town') ||selectedCharacter && <li className="nav-li" onClick={()=>navigate('/town')}><img className='nav-img' src='/Icons/Bag.png' alt='settings' /><p className="nav-p">Town</p></li>}
                </ul>
                {(location.pathname === '/signup') && (
                    <ul className="nav-ul" onClick={handleLogout}>
                        <li className="nav-li" ><img className='nav-img' src='/Icons/signup.png' alt='settings' /><p className="nav-p">Signup or Login</p></li>
                    </ul>
                )}
                {user && (
                    <ul className="nav-ul" onClick={handleLogout}>
                        <li className="nav-li"><img className='nav-img' src='/Icons/doorexit.png' alt='Logout Png'/><p className="nav-p">Logout</p></li>
                    </ul>
                )}
            </div>
    );
}
export default Nav;