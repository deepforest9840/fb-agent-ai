import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import logo from '../Assets/logo.png';
import cart_icon from '../Assets/cart_icon.png';
import { ShopContext } from '../../Context/ShopContext';
import axios from "axios";

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const [menu, setMenu] = useState('shop');
  const [searchValue, setSearchValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { getTotalCartItems } = useContext(ShopContext);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const parameterValue = searchValue.trim() !== '' ? searchValue : selectedCategory;
    window.location.href = `/demo/${parameterValue}`;
  };

  const handleLogout = async () => {
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
  
      // Call the backend logout endpoint to invalidate the token
      const response = await axios.post('http://localhost:8000/logout', {}, config);
      
      // Handle response and token invalidation logic
      console.log('Logout successful:', response.data);
  
      setIsLoggedIn(false); // Update the isLoggedIn state to false
      localStorage.removeItem('accessToken'); // Remove the access token from localStorage
      navigate('/');

    } catch (error) {
      console.error('Logout failed:', error);
    }
  };


  return (
    <div className="navbar">
      <div className="nav-logo">
        <img src={logo} alt="" />
        <p>BidCraft</p>
      </div>
      <form onSubmit={handleSubmit} className="nav-search">
        <input
          type="text"
          placeholder="Search category..."
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
        />
        <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
          <option value="all">All</option>
          <option value="men">Men</option>
          <option value="women">Women</option>
          <option value="kid">Kids</option>
        </select>
        <button type="submit">Search</button>
      </form>
      <ul className="nav-menu">
        <li onClick={() => setMenu('shop')}>
          <Link style={{ textDecoration: 'none' }} to="/">
            Shop
          </Link>
          {menu === 'shop' ? <hr /> : <></>}
        </li>
        <li onClick={() => { setMenu("mens") }}>
          <Link style={{ textDecoration: 'none' }} to='/mens'>Vehicle</Link>
          {menu === "mens" ? <hr /> : <></>}
        </li>
        <li onClick={() => { setMenu("womens") }}>
          <Link style={{ textDecoration: 'none' }} to='/womens'>Electronics</Link>
          {menu === "womens" ? <hr /> : <></>}
        </li>
        <li onClick={() => { setMenu("kids") }}>
          <Link style={{ textDecoration: 'none' }} to='/kids'>Others</Link>
          {menu === "kids" ? <hr /> : <></>}
        </li>
      </ul>
      <div className="nav-login-cart">
        <div className="nav-create-bid">
          <Link to="/createbid">
            <button>Create bid</button>
          </Link>
        </div>
        {isLoggedIn ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/login">
            <button>Login / Signup</button>
          </Link>
        )}
        <Link to="/cart">
          <img src={cart_icon} alt="" />
        </Link>
        <div className="nav-cart-count">{getTotalCartItems()}</div>
      </div>
    </div>
  );
};

export default Navbar;
