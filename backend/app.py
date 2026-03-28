import logging
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from backend.database import db
from backend.routes.rooms import rooms_bp
from backend.routes.bookings import bookings_bp

logging.basicConfig(level=logging.INFO)

def create_app(config_overrides=None):
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    # Register basic API home
    @app.route("/")
    def home():
        return jsonify({
            "data": {"message": "API is running"},
            "error": None
        })

    # Global error handler for JSON API consistency
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        
        # Explicitly checking for 500 error traces to not send them as-is
        if response.status_code == 500:
            error_msg = "An unexpected internal server error occurred"
        else:
            error_msg = e.description
            
        return jsonify({
            "data": None,
            "error": error_msg
        }), e.code

    app.register_blueprint(rooms_bp)
    app.register_blueprint(bookings_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
