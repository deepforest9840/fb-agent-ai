import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import NextPage from './Pages/NextPage'; // Import NextPage
import reportWebVitals from './reportWebVitals';
import ShopContextProvider from './Context/ShopContext';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <ShopContextProvider>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/next" element={<NextPage />} />
      </Routes>
    </Router>
  </ShopContextProvider>
);

reportWebVitals();
