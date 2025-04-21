import React, { useState, useEffect, useContext } from 'react';
import './Item.css';
import { Link } from 'react-router-dom';
import { ShopContext } from '../../Context/ShopContext';

const Item = ({ id, name, image, new_price, old_price, AuctionEndDate,bid }) => {
  const { addToCart } = useContext(ShopContext);
  const [timeLeft, setTimeLeft] = useState(getTimeRemaining(new Date(AuctionEndDate)));

  useEffect(() => {
    if (AuctionEndDate) {
      const timer = setInterval(() => {
        setTimeLeft(getTimeRemaining(new Date(AuctionEndDate)));
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [AuctionEndDate]);

  function getTimeRemaining(endTime) {
    const total = endTime - new Date();
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

  const renderCountdown = () => {
    if (timeLeft.total > 0) {
      const { days, hours, minutes, seconds } = timeLeft;
      return (
        // <p>Time Left: {days} days {hours} hours {minutes} minutes {seconds} seconds</p>
        <p>Running</p>
      );
    } else {
      return <p>Ended</p>;
    }
  };

  return (
    <div className='item'>
      <Link to={`/product/${id}`}>
        <img onClick={() => window.scrollTo(0, 0)} src={image} alt="" />
      </Link> 
      <p>{name}</p>
      <div className="item-prices">
        <div className="item-price-new">
          ${new_price}
        </div> 
        <div className="item-price-old">
          ${old_price}
        </div>
        <div className="item-Auction-End-Date">
          {renderCountdown()}
        </div>
        <div className="item-bid">
          <p>Bid:{bid}</p>
        </div>
      </div>
    </div>
  );
};

export default Item;
