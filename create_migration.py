"""
Create migration for ClassSchedule model
"""
from app import create_app, db
from flask_migrate import Migrate, migrate as flask_migrate, upgrade

app = create_app()
migrate_obj = Migrate(app, db)

with app.app_context():
    # Create migration
    flask_migrate(message="Add ClassSchedule model for weekly Zoom classes")
    print("Migration created successfully!")
    
    # Apply migration
    upgrade()
    print("Migration applied successfully!")
