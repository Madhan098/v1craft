import os
import sqlite3
from app import app, db
from models import init_sample_data

def reset_database():
    """Reset the database and recreate it with the correct schema"""
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables
        db.create_all()
        print("Created all tables with new schema")
        
        # Initialize sample data
        init_sample_data()
        print("Database reset completed successfully!")

if __name__ == "__main__":
    reset_database() 