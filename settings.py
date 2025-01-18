import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
ALLOWED_HOSTS = []

def get_setting(setting_name, default_value=None):
    return os.getenv(setting_name, default_value)

GLOBAL_URL = "https://djangowebsite.com"
LOCAL_THANKS = "Thank you for using our service!"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
