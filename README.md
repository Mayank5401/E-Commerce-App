# 🛒 Django E-commerce Application

A modern, fully functional **e-commerce web application** built with Django, designed for a smooth shopping experience with essential features like product browsing, cart management, checkout, order tracking, and customer reviews.

---

## ✨ Features

- **User Authentication**
  - Sign up, login, logout
  - User profile management
  
- **Product Management**
  - Product listing and details page
  - Search and filter products
  - Product categories
  
- **Shopping Cart**
  - Add to cart
  - Update or remove items
  - Cart persists for logged-in users

- **Order System**
  - Place orders
  - Order history and order detail pages

- **Ratings and Reviews**
  - Users can rate and review products they have purchased
  - Display average product ratings on product pages
  
- **Admin Panel**
  - Manage products, categories, orders, and users via Django admin

- **Responsive UI**
  - Mobile and desktop friendly

- **Order Invoice Genration**
  - Download Invoice in PDF format

---

## 🛠️ Tech Stack

| Layer | Technology |
|:---|:---|
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Backend** | Python 3, Django 4 |
| **Database** | SQLite (default), easy to switch to PostgreSQL |
| **Other** | Django Templates, Django Forms, Static Files Management |

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-django.git
   cd ecommerce-django
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the App**
   - Open your browser and visit: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 📷 Screenshots (optional)
> *(You can add product page, cart page, checkout screenshots later.)*

---

## 📈 Future Improvements
- Payment Gateway Integration (Stripe/PayPal)
- Email Notifications for Orders
- Wishlist and Save for Later
- Coupons and Discounts
- Advanced Search with ElasticSearch
- Product Recommendations

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).


