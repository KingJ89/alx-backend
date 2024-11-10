#!/usr/bin/env python3
"""
A Flask app that displays the current time with localization and timezone support.
"""
import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Union, Dict


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

# Sample users data with locale and timezone preferences
users = {
    1: {"name": "Carol", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Gift", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Jan", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Salomy", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieve a user based on the 'login_as' query parameter."""
    login_id = request.args.get('login_as')
    if login_id and login_id.isdigit():
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the global user before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages:
    - Checks the 'locale' query parameter.
    - Checks the user's locale if logged in.
    - Checks the 'locale' in request headers.
    - Defaults to the application's default locale.
    """
    # Check for 'locale' in query parameters
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale

    # Check the user's preferred locale if available
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']

    # Check for 'locale' in request headers
    header_locale = request.headers.get('locale')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale

    # Default to the configured default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best match for the timezone:
    - Checks the 'timezone' query parameter.
    - Checks the user's preferred timezone if logged in.
    - Defaults to the application's default timezone.
    """
    # Check for 'timezone' in query parameters
    timezone = request.args.get('timezone')
    if not timezone and g.user:
        timezone = g.user['timezone']

    try:
        # Validate the timezone
        if timezone:
            return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        pass

    # Fallback to default timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """
    Renders the home page with the current localized time.
    Template: index.html
    """
    current_time = format_datetime()
    return render_template('index.html', current_time=current_time)


# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

