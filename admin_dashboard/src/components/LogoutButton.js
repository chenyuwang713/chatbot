import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('admin_token');
        navigate('/');
    };

    return (
        <button onClick={handleLogout} style={{ background: 'red', color: 'white', border: 'none', padding: '8px 12px', cursor: 'pointer' }}>
            Logout
        </button>
    );
};

export default LogoutButton;
