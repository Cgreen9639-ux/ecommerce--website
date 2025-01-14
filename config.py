import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'your_stripe_secret_key'
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID') or 'your_paypal_client_id'
    PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET') or 'your_paypal_secret'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
