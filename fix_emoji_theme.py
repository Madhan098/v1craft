from app import app, db
from models import Template

def fix_emoji_theme():
    """Fix any templates with None or empty emoji_theme values"""
    
    with app.app_context():
        # Get all templates
        templates = Template.query.all()
        
        for template in templates:
            if template.emoji_theme is None or template.emoji_theme.strip() == '':
                # Set a default emoji based on event type
                if template.event_type == 'wedding':
                    template.emoji_theme = '💒💍❤️'
                elif template.event_type == 'birthday':
                    template.emoji_theme = '🎂🎉🎈'
                elif template.event_type == 'anniversary':
                    template.emoji_theme = '💑❤️🌹'
                elif template.event_type == 'babyshower':
                    template.emoji_theme = '👶🍼🎀'
                elif template.event_type == 'graduation':
                    template.emoji_theme = '🎓📚🎉'
                elif template.event_type == 'retirement':
                    template.emoji_theme = '👴👵🎊'
                else:
                    template.emoji_theme = '🎉✨🎊'
                
                print(f"Fixed template '{template.name}' - set emoji_theme to '{template.emoji_theme}'")
        
        # Commit changes
        db.session.commit()
        print("All templates fixed successfully!")

if __name__ == "__main__":
    fix_emoji_theme() 