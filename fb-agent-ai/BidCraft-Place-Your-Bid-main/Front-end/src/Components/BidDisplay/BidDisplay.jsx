import React, { useState, useEffect, useContext } from 'react';
import './BidDisplay.css';
import star_icon from '../Assets/star_icon.png';
import star_dull_icon from '../Assets/star_dull_icon.png';
import { ShopContext } from '../../Context/ShopContext';

const BidDisplay = ({ product }) => {
  const { addToCart } = useContext(ShopContext);
  const [timeLeft, setTimeLeft] = useState(getTimeRemaining(product.AuctionEndDate));

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(getTimeRemaining(product.AuctionEndDate));
    }, 1000);

    return () => clearInterval(timer);
  }, [product.AuctionEndDate]);

  function getTimeRemaining(endTime) {
    const total = Date.parse(endTime) - Date.parse(new Date());
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const days = Math.floor(total / (1000 * 60 * 60 * 24));

    return {
      total,
      days,
      hours,
      minutes,
      seconds,
    };
  }

  return (
    <div className="biddisplay-container">
      <div className="biddisplay-image">
        <img src={product.image} alt={product.name} />
      </div>
      <div className="biddisplay-details">
        <h3>{product.name}</h3>
        <p>Condition: Used</p>
        <p>Stock Type: Single</p>
        <p>Available Quantity: 1 Piece</p>
        <div className="bidding-details">
          <p>Starting Bid: ${product.old_price} (Reserve Price: ${product.new_price})</p>
          <p>Time Left: {timeLeft.days} days {timeLeft.hours} hours {timeLeft.minutes} minutes {timeLeft.seconds} seconds</p>
          <p>Active Bidders: 0 Total Bid: $0</p>
          <div className="bid-section">
            <p>Enter your available bid (it's free)</p>
            <input type="text" placeholder="Bid Amount" />
            <button onClick={() => addToCart(product.id)}>Place Bid</button>
            <p>Or</p>
            <button>Place an automatic bid</button>
          </div>
          <p>Buy Now Price: $6200,000</p>
        </div>
      </div>
    </div>
  );
};

export default BidDisplay;
