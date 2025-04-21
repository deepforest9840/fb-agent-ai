import React, { useState } from 'react';
import axios from 'axios';
import './CSS/ChangePassword.css';

const ChangePassword = () => {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmNewPassword: '',
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
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('Access token not found');
        return;
      }

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      const response = await axios.put('http://localhost:8000/change_password',
        {
          password: formData.newPassword,
          confirm_password: formData.confirmNewPassword,
        },
        config
      );

      console.log('Password change successful:', response.data);
      alert('Password updated successfully.');
    } catch (error) {
      console.error('Password change failed:', error.response);
      alert('Failed to update password. Please try again.');
    }
  };

  return (
    <div className="change-password">
      <div className="change-password-container">
        <h2>Change Password</h2>
        <form onSubmit={handleSubmit}>
          <div className="change-password-fields">
            <input
              type="password"
              name="currentPassword"
              placeholder="Current Password"
              value={formData.currentPassword}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="newPassword"
              placeholder="New Password"
              value={formData.newPassword}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="confirmNewPassword"
              placeholder="Confirm New Password"
              value={formData.confirmNewPassword}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit">Change Password</button>
        </form>
      </div>
    </div>
  );
};

export default ChangePassword;
