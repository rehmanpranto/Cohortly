"""
Fix UUID column types in the database
This script will drop tables and recreate them with proper UUID types
"""
import psycopg

# Database connection string (from config.py)
DATABASE_URL = 'postgresql://neondb_owner:npg_U3HCRaThw6JY@ep-falling-shadow-a1v2rodx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

print("🔄 Connecting to database...")

try:
    # Connect to database
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("✅ Connected to database")
    
    # Drop all tables (cascade to handle foreign keys)
    print("\n🗑️  Dropping all existing tables...")
    
    tables = [
        'certificates', 'notifications', 'announcements',
        'grades', 'submissions', 'assignments', 'attendance',
        'resources', 'lessons', 'modules', 'payments', 'enrollments',
        'mentor_batches', 'instructor_batches', 'batches', 'bootcamps',
        'lead_logs', 'leads', 'refresh_tokens', 'users'
    ]
    
    for table in tables:
        try:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"   ✓ Dropped {table}")
        except Exception as e:
            print(f"   ⚠️  Could not drop {table}: {str(e)}")
    
    conn.commit()
    print("\n✅ All tables dropped successfully!")
    print("\n📝 Now run the init_db.py script to recreate tables with proper UUID types")
    print("   Command: python app/seeds/init_db.py")
    
    # Close connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    if 'conn' in locals():
        conn.rollback()
    exit(1)
