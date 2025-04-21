import React, { useState } from 'react';
import axios from 'axios';
import './CSS/ForgetPassword.css';

const ForgetPassword = () => {
  const [formData, setFormData] = useState({
    email: '',
  });

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
      const response = await axios.post('http://localhost:8000/forget_password', {
        user_id: formData.email,  // Assuming server expects 'user_id' for email
      });

      console.log('Password recovery request successful:', response.data);
      alert(response.data);
    } catch (error) {
      console.error('Password recovery request failed:', error.response);
      alert('Failed to recover password. Please try again.');
    }
  };

  return (
    <div className="forget-password">
      <div className="forget-password-container">
        <h2>Forget Password</h2>
        <form onSubmit={handleSubmit}>
          <div className="forget-password-fields">
            <input
              type="text"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit">Recover Password</button>
        </form>
        <div className="forget-password-login">
          Remember your password? <span>Login</span>
        </div>
      </div>
    </div>
  );
};

export default ForgetPassword;
