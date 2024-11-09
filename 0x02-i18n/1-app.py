#!/usr/bin/env python3
"""
Basic Babel setup with Flask.
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration class for setting up supported languages and Babel defaults."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel for localization
babel = Babel(app)


@app.route('/')
def index() -> str:
    """Render the home/index page."""
    return render_template('1-index.html')


# Entry point to run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
