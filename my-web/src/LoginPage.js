
import React, { useState } from 'react';
import './LoginPage.css';
import axios from 'axios'; // Will be used for login
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [username, setusername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/login', {
        username: username,  // 👈 use user_id instead of email
        password: password
      });
      
      console.log('Login success:', res.data);
      // Save user data (e.g., JWT token) if necessary
      navigate('/dashboard', { state: { user: res.data.user } });  // Redirect to dashboard
    } catch (err) {
      console.error('Login failed:', err.response?.data || err.message);
      setError('Login failed: Invalid credentials');
    }
  };

  return (
    <div className="login-page">
    <div className="login-container">
      
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>User Name:</label> 
        <input
          type="text"
          value={username}
          onChange={(e) => setusername(e.target.value)}
          required
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
    </div>
  );
}
