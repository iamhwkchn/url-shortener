from flask import Flask
def create_app(test_config = None):
    app = Flask(__name__)
    app.secret_key = 'ds9d9sdf7dfv9sd0fsd07f9ds7dda0q'
    from . import urlshort
    app.register_blueprint(urlshort.bp)
    return app