# BidCraft

BidCraft is an online auction platform where sellers can create auctions for their products, and buyers can place bids on active auctions. This project is developed using React for the frontend, FastAPI for the backend, and SQLite for the database.

## Features

- **User Authentication**:
  - Users can sign up and log in securely to access the platform.
  - Token-based authentication using JSON Web Tokens (JWT) to protect routes.

- **Seller Functionality**:
  - Sellers can create auctions by specifying product details and auction duration.
  - Ability to view and manage active auctions, including updating auction details or ending auctions early.

- **Buyer Functionality**:
  - Buyers can browse active auctions and place bids on products they are interested in.
  - Real-time updates on auction status and bidding activity.

- **Profile Management**:
  - Users can view their profile information, including personal details and auction history.

## Tech Stack

- **Frontend**:
  - React.js
  - React Router for navigation
  - Axios for handling HTTP requests
  - Bootstrap or Material-UI for UI components

- **Backend**:
  - FastAPI (Python) for REST API development
  - SQLite for database management
  - SQLAlchemy for ORM (Object-Relational Mapping)

## Getting Started

### Prerequisites

- Node.js and npm installed globally
- Python 3.x and pip installed

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/bidcraft.git
   cd bidcraft
