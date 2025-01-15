from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from models import User, Product
import stripe
import paypalrestsdk
from config import Config

# Configure Stripe API
stripe.api_key = Config.STRIPE_SECRET_KEY

# Configure PayPal API
paypalrestsdk.configure({
    "mode": "sandbox",  # "live" for production
    "client_id": Config.PAYPAL_CLIENT_ID,
    "client_secret": Config.PAYPAL_SECRET
})

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
            if link.rel == '

if __name__ == "__main__":
    app.run
    