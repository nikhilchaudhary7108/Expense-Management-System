import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <h2>EMS</h2>
      <ul>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/expenses">Expenses</Link></li>
        <li><Link to="/income">Income</Link></li>
        <li><Link to="/transactions">Transactions</Link></li>
        <li><Link to="/categories">Categories</Link></li>
        <li><Link to="/budget">Budget</Link></li>
        <li><Link to="/graph">Analytics</Link></li>
        <li><Link to="/profile">Profile</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
