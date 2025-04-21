import React, { useState } from 'react';
import './CreateBidc.css';
import all_product from '../Assets/all_product';

const CreateBidc = () => {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    new_price: '',
    old_price: '',
    AuctionEndDate: '',
    seller_id: '',
    bid: '',
    image: null, // Add image state
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFormData({
      ...formData,
      image: URL.createObjectURL(file),
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newProduct = {
      name: formData.name,
      category: formData.category,
      new_price: formData.new_price,
      old_price: formData.old_price,
      AuctionEndDate: formData.AuctionEndDate,
      seller_id: formData.seller_id,
      bid: formData.bid,
      image: formData.image, // Include image in the new product
    };

    // Store the new product in local storage or send it to a server
    // Here, let's assume you store it in local storage
    const products = JSON.parse(localStorage.getItem('allProducts')) || [];
    localStorage.setItem('allProducts', JSON.stringify([...products, newProduct]));

    // Reset form data
    setFormData({
      name: '',
      category: '',
      new_price: '',
      old_price: '',
      AuctionEndDate: '',
      seller_id: '',
      bid: '',
      image: null,
    });
  };

  return (
    <div className='create-bidc'>
      <h2>Create Bid</h2>
      <form onSubmit={handleSubmit}>
        {/* Form inputs */}
        {/* Include image input */}
        <input type='file' name='image' onChange={handleImageChange} />
        {formData.image && <img src={formData.image} alt='Uploaded' />}
        <input type='text' name='name' placeholder='Product Name' value={formData.name} onChange={handleChange} />
        <input type='text' name='category' placeholder='Category' value={formData.category} onChange={handleChange} />
        <input type='number' name='new_price' placeholder='New Price' value={formData.new_price} onChange={handleChange} />
        <input type='number' name='old_price' placeholder='Old Price' value={formData.old_price} onChange={handleChange} />
        <input type='datetime-local' name='AuctionEndDate' value={formData.AuctionEndDate} onChange={handleChange} />
        <input type='text' name='seller_id' placeholder='Seller ID' value={formData.seller_id} onChange={handleChange} />
        <input type='number' name='bid' placeholder='Bid' value={formData.bid} onChange={handleChange} />
        <button type='submit' className='submit-button'>Submit</button>
      </form>
    </div>
  );
};

export default CreateBidc;
