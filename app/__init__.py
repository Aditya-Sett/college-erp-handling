# App Factory

from flask import Flask
from app.config import Config
from app.extensions import init_extensions
from app.routes import register_routes
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)
    register_routes(app)

    return app
