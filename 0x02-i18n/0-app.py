#!/usr/bin/env python3
"""
Basic Flask app: Setting up a basic Flask application.
"""
from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index() -> str:
    """Render the home/index page."""
    return render_template('0-index.html')


# Entry point for running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
