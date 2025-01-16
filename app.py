from flask import Flask, render_template, send_from_directory
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    if Config.CUSTOM_DOMAIN:
        app.run(debug=True, host=Config.CUSTOM_DOMAIN, port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
