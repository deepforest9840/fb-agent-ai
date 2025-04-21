import React from 'react';
import './Test.css'; // Import the renamed CSS file

const Test = () => {  // Renamed Product to Test
  return (
    <div className="product-container">
      <div className="product-image">
        <img src="https://example.com/motorcycle.jpg" alt="Yamaha FZS-FI" />
      </div>
      <div className="product-details">
        <h3>Yamaha FZS-FI V2 DD, 2022</h3>
        <p>Condition: Used</p>
        <p>Stock Type: Single</p>
        <p>Available Quantity: 1 Piece</p>
        <div className="bidding-details">
          <p>Starting Bid: &#8377; 180,000 (Reserve Price: &#8377; 194,000)</p>
          <p>Time Left: 03 days 02 hours 55 minutes 02 seconds</p>
          <p>Active Bidders: 0 Total Bid: &#8377; 0</p>
          <div className="bid-section">
            <p>Enter your available bid (it's free)</p>
            <input type="text" placeholder="Bid Amount" />
            <button>Place Bid</button>
            <p>Or</p>
            <button>Place an automatic bid</button>
          </div>
          <p>Buy Now Price: &#8377; 6200,000</p>
        </div>
      </div>
    </div>
  );
};

export default Test;
