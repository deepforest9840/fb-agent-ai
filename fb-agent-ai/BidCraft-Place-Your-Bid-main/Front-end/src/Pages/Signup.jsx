import React, { useState } from 'react';
import axios from 'axios';
import './CSS/Signup.css'; // Import the CSS file
import { Link } from 'react-router-dom';

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    dob: '',
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
      const response = await axios.post('http://localhost:8000/signup', formData);
      console.log('Response:', response); // Log the entire response object
      console.log('Response data:', response.data); // Log response data if available
    } catch (error) {
      console.error('Signup failed:', error); // Log the entire error object
      if (error.response) {
        console.error('Response data:', error.response.data); // Log response data if available
      }
    }
  };
  

  return (
    <div className="signup">
      <div className="signup-container">
        <h2>Signup</h2>
        <form onSubmit={handleSubmit} className="signup-fields">
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="tel"
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
          <input
            type="date"
            name="dob"
            placeholder="Date of Birth"
            value={formData.dob}
            onChange={handleChange}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
        <div className="signup-login">
          Already have an account? <Link to="/login"><span>Login</span></Link>
        </div>
        <div className="signup-agree">
          <input type="checkbox" />
          <label>
            I agree to the <span>Terms and Conditions</span>
          </label>
        </div>
      </div>
    </div>
  );
};

export default Signup;
