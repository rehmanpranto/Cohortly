"""
Flask application factory
"""
import os
import uuid
from flask import Flask, render_template
from flask_login import login_required
from app.config import config
from app.extensions import db, migrate, jwt, login_manager, csrf


def create_app(config_name=None):
    """Application factory"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID. Convert string to UUID for database query."""
        try:
            # Convert string to UUID if needed
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
            # Use session.get() instead of Query.get() for better UUID support
            return db.session.get(User, user_id)
        except (ValueError, AttributeError, TypeError):
            return None
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.crm.routes import crm_bp
    from app.lms.routes import lms_bp
    from app.payments.routes import payments_bp
    from app.analytics.routes import analytics_bp
    from app.certificates.routes import certificates_bp
    from app.student_lifecycle import bp as student_lifecycle_bp
    from app.projects import bp as projects_bp
    from app.portfolio import bp as portfolio_bp
    from app.career import bp as career_bp
    from app.communication import bp as communication_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(crm_bp, url_prefix='/crm')
    app.register_blueprint(lms_bp, url_prefix='/lms')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(certificates_bp, url_prefix='/certificates')
    app.register_blueprint(student_lifecycle_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(communication_bp)
    app.register_blueprint(api_bp)  # Mobile API
    
    # Root route
    @app.route('/')
    def index():
        return render_template('shared/landing.html')
    
    # Features page
    @app.route('/features')
    @login_required
    def features():
        return render_template('shared/features.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('shared/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('shared/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('shared/500.html'), 500
    
    return app
