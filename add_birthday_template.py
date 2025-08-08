
from app import app, db
from models import Template

def add_birthday_template():
    """Add the new birthday template to the database"""
    with app.app_context():
        try:
            # Check if template already exists
            existing_template = Template.query.filter_by(
                name='Simple Birthday Card'
            ).first()
            
            if existing_template:
                print("✅ Template already exists")
                return
            
            # Create new template
            template = Template(
                name='Simple Birthday Card',
                description='Clean and simple birthday card design',
                event_type='birthday',
                religious_type='general',
                style='modern',
                color_scheme='pink',
                font_family='Arial, sans-serif',
                emoji_theme='🎂🎉🎈',
                preview_image='https://via.placeholder.com/300x400/ff6b6b/FFFFFF?text=Simple+Birthday',
                is_active=True,
                usage_count=0
            )
            
            db.session.add(template)
            db.session.commit()
            
            print(f"✅ Successfully added birthday template with ID: {template.id}")
            
        except Exception as e:
            print(f"❌ Failed to add template: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    add_birthday_template()
