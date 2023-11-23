import React from 'react';
import './App.css';


const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <img src="./Logo.png" alt="Tiketi Tamasha" />
        <p>Tiketi Tamasha</p>
      </div>
      <ul className="navbar-nav">
        <li className="nav-item">
          <a href="/learn-more" className="nav-link">Login</a>
        </li>
        <li className="nav-item">
          <a href="/login" className="nav-link">Cart</a>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
