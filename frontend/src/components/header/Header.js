import './Header.css'
import {Link, NavLink} from "react-router-dom";
import logo from './logo.png'

function Header() {
    const exitHundler = () => {
        sessionStorage.clear()
        window.location.assign('/login')
    }
    return (
        <nav>
            <div>
                <p className='logo'><NavLink to='/'><img src={logo} alt='logo'/></NavLink></p>
            </div>
            <div>
                <p><NavLink to='/rates'>Курсы валют</NavLink></p>
                <p><NavLink to='/countries'>Страны</NavLink></p>
                <p onClick={exitHundler}>Выход</p>
            </div>
        </nav>
    );
}

export default Header;
