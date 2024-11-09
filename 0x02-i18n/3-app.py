#!/usr/bin/env python3
"""
A Basic Flask app with Babel for localization.
This application supports English and French translations.
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for Flask-Babel settings."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel with the Flask app
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best match for supported languages
    based on the client's browser settings.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Renders the home/index page.
    Template: 2-index.html
    """
    return render_template('2-index.html')


# Entry point to run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
