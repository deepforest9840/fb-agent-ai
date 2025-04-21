import React, { useState } from 'react';
import axios from 'axios';
import './CSS/Login.css';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate

const Login = ({ setIsLoggedIn }) => { // Pass setIsLoggedIn as a prop
  const [formData, setFormData] = useState({
    user_id: '',
    password: '',
  });

  const navigate = useNavigate(); // Initialize navigate hook

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/signin', formData);
      if (response && response.data && response.data.accessToken) {
        localStorage.setItem('accessToken', response.data.accessToken); // Store token in localStorage
        setIsLoggedIn(true); // Set isLoggedIn state to true
        console.log('Login successful:', response.data);
        // Navigate to home page ('/')
        navigate('/');

      } else {
        console.error('Login failed: Response data is undefined');
      }
    } catch (error) {
      console.error('Login failed:', error);

      if (error.response) {
        console.error('Error response:', error.response.data);
      }
    }
  };

  return (
    <div className="login">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="login-fields">
            <input
              type="text"
              name="user_id"
              placeholder="User ID (Email or Phone)"
              value={formData.user_id}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <div className="forgot-password">
            Forgot Password? <Link to="/forgetpassword"><span>Click Here</span></Link>
          </div>
          <button type="submit">Login</button>
        </form>
        <div className="login-login">
          Don't have an account? <Link to="/signup"><span>Sign Up</span></Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
