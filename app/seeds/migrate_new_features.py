"""
Migration script to add new comprehensive features to the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.extensions import db
from app.models import (
    StudentProfile, PerformanceReview, Project, ProjectSubmission,
    PortfolioItem, JobApplication, AlumniNetwork, Survey, SurveyResponse,
    Message, DiscussionForum, ForumPost, Document
)

def migrate_database():
    """Create all new tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating new tables for comprehensive features...")
        
        # Create all tables
        db.create_all()
        
        print("✓ All new tables created successfully!")
        print("\nNew features added:")
        print("  • Student Profiles with RAG rating")
        print("  • Performance Reviews")
        print("  • Project-Based Learning")
        print("  • Portfolio Management")
        print("  • Job Application Tracking")
        print("  • Alumni Network")
        print("  • Surveys & Feedback")
        print("  • Direct Messaging")
        print("  • Discussion Forums")
        print("  • Document Management")

if __name__ == '__main__':
    migrate_database()
