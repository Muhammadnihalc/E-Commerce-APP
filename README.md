
E - Commerce Web application

This project is an E-commerce web application created in Python with the Flask framework. Users, or customers, can use the application as an online shopping platform to browse a variety of products, view product details, add items to their shopping cart, receive coupon code discounts after every nth order, and check out to place an order and even make the payment online.


## Features


- User Registration and Authentication:
   - Users can register for an account, providing personal details.
   - Secure authentication using Flask-Login and password hashing with bcrypt.

- Product Management:
   - Products categorized and associated with brands.
   - Product details include name, price, discount, stock, colors, description, and images.

- Shopping Cart:
   - Users can add products to the shopping cart.
   - Cart details stored in the user's session for easy review and updates.

- Order Placement:
   - Users can proceed to checkout, generating a unique invoice.
   - Order details, including product list, stored in the database.

- Coupon Code System:
   - Every nth order receives a 10% discount coupon.
   - One time usable unique Coupon code generated and associated with users for future use.

- Coupon Code Validation:
   - Users can apply discount coupons during checkout.
   - System validates coupon authenticity and ownership before applying the discount.

- Payment Integration:
   - Integration with the Stripe API for secure payment processing.
   - Users can make payments using credit/debit cards.

- User Order History:
   - Users can view their order history, including details of past orders.

- Frontend and Navigation:
   - User-friendly frontend designed with Jinja templating and Bootstrap.
   - Different routes for exploring products, viewing details, and managing orders.

- Dynamic Product Filtering:
    - Products can be filtered based on categories and brands.
    - Enhances user experience by providing specific product categories.

- Profile Picture Upload:
    - Users can upload profile pictures during registration.
    - Profile pictures stored for user customization.

- Flash Messages:
    - Flash messages for providing feedback on successful actions or error messages.
    - Enhances user communication and experience.

- Logout and Session Management:
    - Users can log out of their accounts securely.
    - Session management for maintaining user state.
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/Muhammadnihalc/E-Commerce-APP
```

Create a Virtual Environment:

```bash
  python -m venv venv
```

Install requirement.txt file

```bash
  pip install -r requirements.txt

```

Start the server

```bash
  flask run

```


## Note

- Remember to enter'secret123' in the company_secret_code column when utilising the '/register' route for the admin registration. This strategy was implemented to stop outside users from registering as administrators through the '/register' route. You can set up your own unique business secret code just go the src/admin/routes.py code then find '/register' route and modify your custom secret code


-  As you approach "/payment," you will be prompted to enter your card information to complete the payment. Please keep in mind that this is a test mode and that your card information will not be saved. Your card number may be validated, but even though this is a test mode, it is advised that don't share your CVV number and other sensitive information.

 
