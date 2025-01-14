# An Apple eStore

**An Apple eStore** is a fully functional e-commerce platform for purchasing Apple products. The application provides features such as user authentication, shopping cart management, an order summary, and a secure checkout process with proof-of-payment uploads.

---

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **Product Catalog**: View and filter available Apple products.
- **Shopping Cart**: Add, update, and remove items dynamically from the cart.
- **Order Summary**: Detailed view of items, quantities, and total price during checkout.
- **Proof of Payment**: Upload proof of payment (PDF format) to complete the checkout process.
- **Responsive Design**: Optimized for desktop and mobile devices.
- **Secure Transactions**: Uses Django's built-in security features for session management and file handling.

---

## Technologies Used

### Frontend
- **HTML5** and **CSS3**
- **Bootstrap** for responsive design
- **JavaScript** for dynamic interactions

### Backend
- **Django Framework**: Manages server-side logic, user authentication, and database interactions.
- **SQLite**: Database for storing product, user, and order information.

### Additional Tools
- **Django Templates**: For rendering dynamic HTML pages.
- **Django FileSystemStorage**: For handling proof-of-payment uploads.
- **Session Management**: Tracks user-specific cart data.

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/an-apple-estore.git
   cd an-apple-estore
2. **Set up a virtual environment**:
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
3. **Apply migrations**:
   python manage.py migrate
4. **Run the development server**:
   python manage.py runserver
5. **Access the application:**
   Open your browser and navigate to http://127.0.0.1:8000/

