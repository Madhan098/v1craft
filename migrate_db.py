
from app import app, db
from models import Invitation, Template
from sqlalchemy import text

def migrate_database():
    """Add all missing columns to invitations and templates tables"""
    with app.app_context():
        try:
            # Check and add religious_type column to invitations table
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='invitations' AND column_name='religious_type'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE invitations 
                    ADD COLUMN religious_type VARCHAR(50) DEFAULT 'general'
                """))
                print("✅ Added religious_type column to invitations")
            else:
                print("✅ religious_type column already exists in invitations")
            
            # Check and add religious_type column to templates table
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='templates' AND column_name='religious_type'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE templates 
                    ADD COLUMN religious_type VARCHAR(50) DEFAULT 'general'
                """))
                print("✅ Added religious_type column to templates")
            else:
                print("✅ religious_type column already exists in templates")
            
            # Check and add family_name column to invitations
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='invitations' AND column_name='family_name'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE invitations 
                    ADD COLUMN family_name VARCHAR(200)
                """))
                print("✅ Added family_name column to invitations")
            else:
                print("✅ family_name column already exists in invitations")
            
            # Check and add main_image column to invitations
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='invitations' AND column_name='main_image'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE invitations 
                    ADD COLUMN main_image VARCHAR(255)
                """))
                print("✅ Added main_image column to invitations")
            else:
                print("✅ main_image column already exists in invitations")
            
            # Check and add gallery_images column to invitations
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='invitations' AND column_name='gallery_images'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE invitations 
                    ADD COLUMN gallery_images TEXT
                """))
                print("✅ Added gallery_images column to invitations")
            else:
                print("✅ gallery_images column already exists in invitations")
            
            # Check and add font_family column to templates
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='templates' AND column_name='font_family'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE templates 
                    ADD COLUMN font_family VARCHAR(100)
                """))
                print("✅ Added font_family column to templates")
            else:
                print("✅ font_family column already exists in templates")
            
            # Check and add emoji_theme column to templates
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='templates' AND column_name='emoji_theme'
            """))
            
            if not result.fetchone():
                db.session.execute(text("""
                    ALTER TABLE templates 
                    ADD COLUMN emoji_theme VARCHAR(100)
                """))
                print("✅ Added emoji_theme column to templates")
            else:
                print("✅ emoji_theme column already exists in templates")
            
            # Update existing records to have default values
            db.session.execute(text("""
                UPDATE invitations 
                SET religious_type = 'general' 
                WHERE religious_type IS NULL
            """))
            
            db.session.execute(text("""
                UPDATE templates 
                SET religious_type = 'general' 
                WHERE religious_type IS NULL
            """))
            
            db.session.commit()
            print("✅ Successfully migrated database tables")
                
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()
