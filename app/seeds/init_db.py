"""
Database initialization script.
Run this to create all tables in the database.
"""
from app import create_app
from app.extensions import db

def init_db():
    """Initialize the database by creating all tables."""
    app = create_app()
    
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nNext steps:")
        print("1. Run: python -m app.seeds.create_admin")
        print("2. Start the server: flask run")

if __name__ == '__main__':
    init_db()
