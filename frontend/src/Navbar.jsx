import './css/navbar.css';
import './css/genericStyles.css';
import { useNavigate } from 'react-router';

// TODO @dyasin: Don't display certain buttons if we are not admin
const Navbar = () => {
    let navigate = useNavigate();

    return (
        <div className='navbar'>
            <div onClick={() => navigate('/')} className='button'>
                MunchMate
            </div>
            <div onClick={() => navigate('/add-restaurant')} className='button'>
                Add Restaurant
            </div>
        </div>
    );
}

export default Navbar;
