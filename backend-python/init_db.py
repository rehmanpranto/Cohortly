"""
Database Initialization Script
Creates all tables in the PostgreSQL database using SQLAlchemy models.
"""
import sys
from pathlib import Path

# Add the backend-python directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.database import Base, engine
from app.models.user import User
from app.models.bootcamp import Bootcamp
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.lead import Lead

def init_database():
    """Create all database tables."""
    try:
        print("🔄 Starting database initialization...")
        print(f"📊 Database URL: {engine.url}")
        
        # Import all models to ensure they're registered with Base
        print("\n📦 Models loaded:")
        print(f"  - User")
        print(f"  - Bootcamp")
        print(f"  - Enrollment")
        print(f"  - Assignment")
        print(f"  - Lead")
        
        # Create all tables
        print("\n🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Successfully created {len(tables)} tables:")
        for table in tables:
            print(f"  ✓ {table}")
        
        print("\n🎉 Database initialization complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
