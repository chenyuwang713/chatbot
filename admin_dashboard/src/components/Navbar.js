import React from 'react';
import { Link } from 'react-router-dom';
import LogoutButton from './LogoutButton';

const Navbar = ({ token }) => {
    return (
        <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: '#0078D4', color: 'white' }}>
            <h2>Admin Dashboard</h2>
            <div>
                <Link to="/dashboard" style={{ color: 'white', marginRight: '15px' }}>Dashboard</Link>
                <Link to="/upload" style={{ color: 'white', marginRight: '15px' }}>Upload Emails</Link>
                <Link to="/responses" style={{ color: 'white', marginRight: '15px' }}>User Responses</Link>
                {token && <LogoutButton />}
            </div>
        </nav>
    );
};

export default Navbar;