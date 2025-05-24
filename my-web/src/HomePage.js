// HomePage.jsx
import React from 'react';
import './HomePage.css';
import { useNavigate } from 'react-router-dom';

export default function HomePage() {
    const navigate = useNavigate();
  
    return (
        <div className="homepage"> 
      <div className="container">
        <div className="left-panel">
          <h1>Expense <br /> Management System</h1>
          <p>Manage. Analyze. Save Smartly.</p>
        </div>
  
        <div className="right-panel">
          <h2>Already Registered?</h2>
          <button className="LoginButton-button" onClick={() => navigate('/login')}>Login</button>
          <h3>New User?</h3>
          <button className="RegisterButton-button" onClick={() => navigate('/register')}>Register</button>
        </div>
  
        <footer>© 2025 Expense Management System. All rights reserved.</footer>
      </div>
      </div>
    );
  }
  
  
//   export default function HomePage() {
//     return (
//       <Router>
//         <Routes>
//           <Route path="/" element={<HomePage />} />
//           <Route path="/login" element={<LoginPage />} />
//           <Route path="/register" element={<RegisterPage />} />
//           <Route path="/dashboard" element={<DashboardPage />} />
//         </Routes>
//       </Router>
//     );
//   }