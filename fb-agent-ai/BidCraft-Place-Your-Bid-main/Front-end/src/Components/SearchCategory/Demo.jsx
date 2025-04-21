import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import data_product from '../Assets/all_product';
import Item from '../Item/Item';
import './Demo.css';
import dropdown_icon from '../Assets/dropdown_icon.png';

const Demo = () => {
  const { parameter } = useParams();
  const [sortOption, setSortOption] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);

  const handleSortChange = (event) => {
    setSortOption(event.target.value);
  };

  useEffect(() => {
    const filtered = data_product.filter(item => item.category === parameter);
    setFilteredProducts(filtered);
  }, [parameter]);

  const applySorting = (products) => {
    switch (sortOption) {
      case 'priceLowToHigh':
        return products.slice().sort((a, b) => a.new_price - b.new_price);
      case 'priceHighToLow':
        return products.slice().sort((a, b) => b.new_price - a.new_price);
      case 'nameAZ':
        return products.slice().sort((a, b) => a.name.localeCompare(b.name));
      case 'nameZA':
        return products.slice().sort((a, b) => b.name.localeCompare(a.name));
      default:
        return products;
    }
  };

  const sortedProducts = applySorting(filteredProducts);

  return (
    <div className='demo'>
      <p>{parameter}</p>
      <p>amader sdedfdsjfldsk</p>
      <div className="demo-indexSort">
        <p>
          <span>Showing 1-12</span> out of 36 Products
        </p>
        <div className="demo-sort">
          <span>Sort by:</span>
          <select value={sortOption} onChange={handleSortChange}>
            <option value="">Select Option</option>
            <option value="priceLowToHigh">Sort by Price (Low to High)</option>
            <option value="priceHighToLow">Sort by Price (High to Low)</option>
            <option value="nameAZ">Sort by Name (A-Z)</option>
            <option value="nameZA">Sort by Name (Z-A)</option>
          </select>
          <img src={dropdown_icon} alt="" />
        </div>
      </div>
      <div className="demo-item">
        {sortedProducts.map((item, i) => (
          <Item
            key={i}
            id={item.id}
            name={item.name}
            image={item.image}
            new_price={item.new_price}
            old_price={item.old_price}
            AuctionEndDate={item.AuctionEndDate}
          />
        ))}
      </div>
    </div>
  );
}

export default Demo;
