"""
Database Initialization Script
Run this once to create all tables in PostgreSQL
"""
import sys
from pathlib import Path

# Add backend-python to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import Base, engine
from sqlalchemy import inspect

def init_database():
    """Create all database tables"""
    try:
        print("🔄 Initializing database...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Database initialized with {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   ✓ {table}")
        
        print("\n🎉 Database setup complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
