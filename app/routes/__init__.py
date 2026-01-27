# All API Routes

from app.routes.curriculum_routes import curriculum_bp
from app.routes.curriculum_upload_routes import upload_bp

def register_routes(app):
    app.register_blueprint(curriculum_bp, url_prefix="/api/curriculum")
    app.register_blueprint(upload_bp, url_prefix="/api/curriculum")