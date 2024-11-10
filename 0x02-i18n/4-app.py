#!/usr/bin/env python3
"""
A Flask app that uses Babel for localization with forced locale via URL parameter.
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for Babel settings."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best language to use based on the 'locale' query parameter.
    Falls back to the client's preferred language if the parameter is absent or invalid.
    """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index() -> str:
    """
    Renders the home/index page.
    Template: 4-index.html
    """
    return render_template('4-index.html')


# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
