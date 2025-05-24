import React, { useState } from 'react';
import './RegisterPage.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    mobile: '',
    email: '',
    password: ''
  });

  const [step, setStep] = useState(1); // 1: Form, 2: OTP Verification
  const [otp, setOtp] = useState('');
  const [registeredUserId, setRegisteredUserId] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSendOtp = async () => {
    if (!formData.email) return alert("Enter email first");
    
    try {
      // Check if email already exists
      const emailCheckResponse = await axios.post('http://localhost:5000/check-email', { email: formData.email });
      if (emailCheckResponse.data.exists) {
        return alert("Email is already registered");
      }

      // Send OTP
      const res = await axios.post('http://localhost:5000/send-otp', {
        email: formData.email
      });
      alert("OTP sent to your email");
      setStep(2); // show OTP input
    } catch (err) {
      console.error('OTP sending failed:', err);
      alert("Failed to send OTP due to invalid email.");
    }
  };

  const handleVerifyOtp = async () => {
    try {
      const res = await axios.post('http://localhost:5000/verify-otp', {
        email: formData.email,
        otp: otp
      });
      alert("OTP verified");
      handleRegister(); // proceed with actual registration
    } catch (err) {
      console.error('OTP verification failed:', err);
      alert(err.response?.data?.error || "OTP verification failed");
    }
  };

  const handleRegister = async () => {
    if (formData.password.length < 6) {
      alert("Password must be at least 6 characters");
      return;
    }

    try {
      const res = await axios.post('http://localhost:5000/register', {
        full_name: formData.name,
        username: formData.username,
        mobile_no: formData.mobile,
        email: formData.email,
        password: formData.password
      });

      alert("Registration successful!");
      // setRegisteredUserId(res.data.user_id);
      setRegisteredUserId(res.data.user_id); // Set user_id to display
      setStep(3); // Go to step 3: success screen
// Redirect to login page after successful registration
    } catch (err) {
      console.error('Registration failed:', err);
      alert(err.response?.data?.error || "Registration failed");
    }
  };

  const goToLogin = () => navigate('/login');

  return (
    <div className="register-container">
      <h2>Register</h2>

      {step === 1 && (
        <form onSubmit={(e) => e.preventDefault()}>
          <label>Full Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />

          <label>Username:</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} required />

          <label>Mobile No.:</label>
          <input type="tel" name="mobile" value={formData.mobile} onChange={handleChange} required />

          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />

          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />

          <button type="button" onClick={handleSendOtp}>Send OTP on email</button>
        </form>
      )}

      {step === 2 && (
        <div className="otp-verification">
          <label>Enter OTP:</label>
          <input type="text" value={otp} onChange={(e) => setOtp(e.target.value)} required />

          <button onClick={handleVerifyOtp}>Verify OTP</button>
        </div>
      )}

{step === 3 && registeredUserId && (
  <div className="success-box">
    <h3>Registration Successful!</h3>
    <p><strong>Your User ID:</strong> {registeredUserId}</p>
    <button className="login-button" onClick={goToLogin}>Go to Login</button>
  </div>
)}
    </div>
  );
}


// import React, { useState } from 'react';
// import './RegisterPage.css';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';

// export default function RegisterPage() {
//   const [formData, setFormData] = useState({
//     name: '',
//     username: '',
//     mobile: '',
//     email: '',
//     password: ''
//   });

//   const [registeredUserId, setRegisteredUserId] = useState(null);
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData(prev => ({ ...prev, [name]: value }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (formData.password.length < 6) {
//       alert("Password must be at least 6 characters");
//       return;
//     }

//     try {
//       const res = await axios.post('http://localhost:5000/register', {
//         full_name: formData.name,
//         username: formData.username,
//         mobile_no: formData.mobile,
//         email: formData.email,
//         password: formData.password
//       });

//       console.log("Registration success:", res.data);
//       alert("Registration successful!");
//       setRegisteredUserId(res.data.user_id); // Store user_id to display
//     } catch (err) {
//       console.error('Registration failed:', err.response?.data || err.message);
//       alert(err.response?.data?.error || "Registration failed");
//     }
//   };

//   const goToLogin = () => {
//     navigate('/login');
//   };

//   return (
//     <div className="register-container">
//       <h2>Register</h2>
//       <form onSubmit={handleSubmit}>
//         <label>Full Name:</label>
//         <input
//           type="text"
//           name="name"
//           value={formData.name}
//           onChange={handleChange}
//           required
//         />

//         <label>Username:</label>
//         <input
//           type="text"
//           name="username"
//           value={formData.username}
//           onChange={handleChange}
//           required
//         />

//         <label>Mobile No.:</label>
//         <input
//           type="tel"
//           name="mobile"
//           value={formData.mobile}
//           onChange={handleChange}
//           required
//         />

//         <label>Email:</label>
//         <input
//           type="email"
//           name="email"
//           value={formData.email}
//           onChange={handleChange}
//           required
//         />

//         <label>Password:</label>
//         <input
//           type="password"
//           name="password"
//           value={formData.password}
//           onChange={handleChange}
//           required
//           minLength={6}
//         />

//         <button type="submit">Register</button>
//       </form>

//       {registeredUserId && (
//         <div className="success-box">
//           <p><strong>User ID:</strong> {registeredUserId}</p>
//           <button className="login-button" onClick={goToLogin}>Go to Login</button>
//         </div>
//       )}
//     </div>
//   );
// }
