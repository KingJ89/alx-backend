#!/usr/bin/env python3
"""
A Basic Flask app with Babel for localization.
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

# Initialize Babel for the Flask app
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """Render the home/index page."""
    return render_template('2-index.html')


# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
