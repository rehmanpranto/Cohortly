"""
Seed script to create the class_schedules table and add sample data
"""
from app import create_app, db
from datetime import datetime, date, time, timedelta
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Create the table
    with db.engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS class_schedules (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            batch_id UUID NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
            week_number INTEGER NOT NULL,
            class_date DATE NOT NULL,
            class_time TIME NOT NULL,
            duration_minutes INTEGER DEFAULT 120,
            topic VARCHAR(255) NOT NULL,
            description TEXT,
            zoom_link TEXT NOT NULL,
            zoom_meeting_id VARCHAR(100),
            zoom_passcode VARCHAR(50),
            recording_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))
        conn.commit()
    
    print("✓ class_schedules table created successfully!")
    
    # Add sample class schedules for existing batches
    from app.models import Batch
    
    batches = Batch.query.limit(3).all()
    
    if batches:
        with db.engine.connect() as conn:
            for batch in batches:
                start_date = batch.start_date
                
                # Create 12 weeks of classes
                for week in range(1, 13):
                    class_date = start_date + timedelta(weeks=week-1)
                    
                    # Monday and Wednesday classes
                    for day_offset in [0, 2]:  # Monday and Wednesday
                        actual_date = class_date + timedelta(days=day_offset)
                        
                        conn.execute(text("""
                        INSERT INTO class_schedules 
                        (batch_id, week_number, class_date, class_time, duration_minutes, topic, description, zoom_link, zoom_meeting_id, zoom_passcode)
                        VALUES 
                        (:batch_id, :week_number, :class_date, :class_time, :duration, :topic, :description, :zoom_link, :meeting_id, :passcode)
                        """), {
                            'batch_id': str(batch.id),
                            'week_number': week,
                            'class_date': actual_date,
                            'class_time': time(19, 0),  # 7:00 PM
                            'duration': 120,
                            'topic': f'Week {week}: {"Introduction to Python" if week <= 4 else "Advanced Concepts" if week <= 8 else "Capstone Project"}',
                            'description': f'Interactive live session for Week {week} covering key concepts and hands-on practice.',
                            'zoom_link': f'https://zoom.us/j/{9876543210 + week}',
                            'meeting_id': f'{9876543210 + week}',
                            'passcode': f'pass{week:02d}'
                        })
                
                print(f"✓ Added 24 class schedules for batch: {batch.name}")
            
            conn.commit()
    
    print("\n✅ All class schedules created successfully!")
