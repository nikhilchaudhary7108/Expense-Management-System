import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import HomePage from './HomePage';

import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import DashboardPage from './pages/DashboardPage';
import GraphicalViewPage from './pages/GraphicalViewPage';




// function HomePage() {
//   const navigate = useNavigate();

//   return (
//     <div className="container">
//       <div className="left-panel">
//         <h1>Expense <br /> Management System</h1>
//         <p>Manage. Analyze. Save Smartly.</p>
//       </div>

//       <div className="right-panel">
//         <h2>Already Registered?</h2>
//         <button className="LoginButton-button" onClick={() => navigate('/login')}>Login</button>
//         <h3>New User?</h3>
//         <button className="RegisterButton-button" onClick={() => navigate('/register')}>Register</button>
//       </div>

//       <footer>© 2025 Expense Management System. All rights reserved.</footer>
//     </div>
//   );
// }


export default function MyApp() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/graphical-view" element={<GraphicalViewPage />} />

      </Routes>
    </Router>
  );
}

// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
// import './App.css';
// import LoginPage from './LoginPage';
// import RegisterPage from './RegisterPage';
// import DashboardPage from './pages/DashboardPage';
// import ExpensePage from './pages/ExpensePage';
// import IncomePage from './pages/IncomePage';
// import TransactionPage from './pages/TransactionPage';
// import CategoryPage from './pages/CategoryPage';
// import BudgetPage from './pages/BudgetPage';
// import ProfilePage from './pages/ProfilePage';
// import GraphPage from './pages/GraphPage';

// function HomePage() {
//   const navigate = useNavigate();

  
//   return (
//     <div className="container">
//       <h1>Expense <br /> Management System</h1>
//       <h2>If you are already registered</h2>
//       <button className="LoginButton-button" onClick={() => navigate('/login')}>Login</button>
//       <h3>New User?</h3>
//       <button className="RegisterButton-button" onClick={() => navigate('/register')}>Register</button>
//       <footer>
//         © 2025 Expense Management System. All rights reserved.
//       </footer>
//     </div>
//   );
// }

// export default function MyApp() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<HomePage />} />
//         <Route path="/login" element={<LoginPage />} />
//         <Route path="/register" element={<RegisterPage />} />
//         <Route path="/dashboard" element={<DashboardPage />} />
//         <Route path="/expenses" element={<ExpensePage />} />
//         <Route path="/income" element={<IncomePage />} />
//         <Route path="/transactions" element={<TransactionPage />} />
//         <Route path="/categories" element={<CategoryPage />} />
//         <Route path="/budget" element={<BudgetPage />} />
//         <Route path="/profile" element={<ProfilePage />} />
//         <Route path="/graph" element={<GraphPage />} />
//       </Routes>
//     </Router>
//   );
// }
