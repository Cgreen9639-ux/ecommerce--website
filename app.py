from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import stripe
import paypalrestsdk
from models import User, Product
from config import Config

# Initialize the Flask app, SQLAlchemy, and LoginManager
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure Stripe API
stripe.api_key = Config.STRIPE_SECRET_KEY

# Configure PayPal API
paypalrestsdk.configure({
    "mode": "sandbox",  # "live" for production
    "client_id": Config.PAYPAL_CLIENT_ID,
    "client_secret": Config.PAYPAL_SECRET
})

# Define the User model for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for home page (listing products)
@app.route('/page/<int:page_num>', methods=['GET'])
def page(page_num):
    items_per_page = 10
    items = Product.query.paginate(page=page_num, per_page=items_per_page)
    return render_template('index.html', items=items.items, page_num=page_num)

# Route to view product details (AJAX for product details)
@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url
    })

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('page', page_num=1))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash("Login successful!", "success")
            return redirect(url_for('page', page_num=1))  # Redirect to the first page of products
        else:
            flash("Invalid login credentials", "danger")

    return render_template('login.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Route for checkout page
@app.route('/checkout')
@login_required
def checkout():
    # Here we will handle displaying the checkout process.
    return render_template('checkout.html')

# Route for Stripe payment
@app.route('/buy/stripe', methods=['POST'])
@login_required
def buy_stripe():
    try:
        amount = 1000  # This is just an example amount (in cents)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method=request.form['payment_method_id'],
            confirm=True
        )
        flash("Payment successful!", "success")
        return redirect(url_for('page', page_num=1))  # Redirect to the first page after successful payment
    except stripe.error.CardError as e:
        flash(f"Payment failed: {e.error.message}", "danger")
        return redirect(url_for('page', page_num=1))  # Redirect back to the product page if payment fails

# Route for PayPal payment
@app.route('/pay/paypal', methods=['POST'])
@login_required
def pay_paypal():
    amount = '10.00'  # Set the amount to be paid (this should be dynamic in a real store)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "USD"
            },
            "description": "Purchase from Flask Store"
        }],
        "redirect_urls": {
            "return_url": url_for('paypal_success', _external=True),
            "cancel_url": url_for('paypal_cancel', _external=True)
        }
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                approval_url = link.href
                return redirect(approval_url)

    flash("Payment failed", "danger")
    return redirect(url_for('page', page_num=1))

# Route for PayPal success callback
@app.route('/paypal_success')
@login_required
def paypal_success():
    flash("Payment successful!", "success")
    return redirect(url_for('page', page_num=1))

# Route for PayPal cancel callback
@app.route('/paypal_cancel')
@login_required
def paypal_cancel():
    flash("Payment canceled.", "warning")
    return redirect(url_for('page', page_num=1))

# Route for adding a product to cart (this will require a cart system, for simplicity, we will use session)
@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    # Here you can implement cart logic, such as adding the product to a session or database cart
    flash(f'{product.name} has been added to your cart!', 'success')
    return redirect(url_for('page', page_num=1))

# Route for viewing the cart (simple version)
@app.route('/cart', methods=['GET'])
@login_required
def view_cart():
    # Here, you would retrieve cart items from the session or database
    return render_template('cart.html')

# WSGI entry point for deployment
def create_app():
    return app

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
