
from app import app, db
from models import Template

def add_more_templates():
    """Add 1-2 additional templates for each event type"""
    with app.app_context():
        try:
            templates_to_add = [
                # Wedding Templates
                {
                    'name': 'Elegant Hindu Mandap',
                    'description': 'Beautiful mandap design with marigold decorations',
                    'event_type': 'wedding',
                    'religious_type': 'hindu',
                    'style': 'elegant',
                    'color_scheme': 'orange',
                    'font_family': 'Playfair Display, serif',
                    'emoji_theme': '🕉️🌺💐',
                    'preview_image': 'https://via.placeholder.com/300x400/FF8C00/FFFFFF?text=Elegant+Mandap',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Nikah Ceremony',
                    'description': 'Islamic wedding invitation with beautiful calligraphy',
                    'event_type': 'wedding',
                    'religious_type': 'muslim',
                    'style': 'traditional',
                    'color_scheme': 'green',
                    'font_family': 'Amiri, serif',
                    'emoji_theme': '☪️🕌💚',
                    'preview_image': 'https://via.placeholder.com/300x400/228B22/FFFFFF?text=Nikah+Ceremony',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Birthday Templates
                {
                    'name': 'Colorful Birthday Bash',
                    'description': 'Vibrant party invitation with balloons and confetti',
                    'event_type': 'birthday',
                    'religious_type': 'general',
                    'style': 'fun',
                    'color_scheme': 'rainbow',
                    'font_family': 'Fredoka One, cursive',
                    'emoji_theme': '🎉🎈🎁',
                    'preview_image': 'https://via.placeholder.com/300x400/FF1493/FFFFFF?text=Colorful+Bash',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Milestone Birthday',
                    'description': 'Elegant design for special milestone birthdays',
                    'event_type': 'birthday',
                    'religious_type': 'general',
                    'style': 'elegant',
                    'color_scheme': 'gold',
                    'font_family': 'Georgia, serif',
                    'emoji_theme': '🎂✨🥂',
                    'preview_image': 'https://via.placeholder.com/300x400/FFD700/000000?text=Milestone+Birthday',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Anniversary Templates
                {
                    'name': 'Love Story Anniversary',
                    'description': 'Romantic design celebrating years of love',
                    'event_type': 'anniversary',
                    'religious_type': 'general',
                    'style': 'romantic',
                    'color_scheme': 'red',
                    'font_family': 'Dancing Script, cursive',
                    'emoji_theme': '💕❤️🌹',
                    'preview_image': 'https://via.placeholder.com/300x400/DC143C/FFFFFF?text=Love+Story',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Silver Jubilee',
                    'description': 'Classic design for 25th anniversary celebration',
                    'event_type': 'anniversary',
                    'religious_type': 'general',
                    'style': 'classic',
                    'color_scheme': 'silver',
                    'font_family': 'Playfair Display, serif',
                    'emoji_theme': '💎💍👑',
                    'preview_image': 'https://via.placeholder.com/300x400/C0C0C0/000000?text=Silver+Jubilee',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Baby Shower Templates
                {
                    'name': 'Little Prince',
                    'description': 'Royal blue theme for baby boy shower',
                    'event_type': 'babyshower',
                    'religious_type': 'general',
                    'style': 'cute',
                    'color_scheme': 'blue',
                    'font_family': 'Quicksand, sans-serif',
                    'emoji_theme': '👑👶💙',
                    'preview_image': 'https://via.placeholder.com/300x400/4169E1/FFFFFF?text=Little+Prince',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Little Princess',
                    'description': 'Pink and gold theme for baby girl shower',
                    'event_type': 'babyshower',
                    'religious_type': 'general',
                    'style': 'cute',
                    'color_scheme': 'pink',
                    'font_family': 'Quicksand, sans-serif',
                    'emoji_theme': '👑👸💖',
                    'preview_image': 'https://via.placeholder.com/300x400/FFB6C1/000000?text=Little+Princess',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Graduation Templates
                {
                    'name': 'Achievement Unlocked',
                    'description': 'Modern graduation celebration design',
                    'event_type': 'graduation',
                    'religious_type': 'general',
                    'style': 'modern',
                    'color_scheme': 'blue',
                    'font_family': 'Montserrat, sans-serif',
                    'emoji_theme': '🎓📚🏆',
                    'preview_image': 'https://via.placeholder.com/300x400/1E90FF/FFFFFF?text=Achievement+Unlocked',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Scholar\'s Pride',
                    'description': 'Traditional academic achievement celebration',
                    'event_type': 'graduation',
                    'religious_type': 'general',
                    'style': 'traditional',
                    'color_scheme': 'gold',
                    'font_family': 'Georgia, serif',
                    'emoji_theme': '🎓🏅📜',
                    'preview_image': 'https://via.placeholder.com/300x400/DAA520/FFFFFF?text=Scholar+Pride',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Retirement Templates
                {
                    'name': 'Well Deserved Rest',
                    'description': 'Warm and appreciative retirement celebration',
                    'event_type': 'retirement',
                    'religious_type': 'general',
                    'style': 'warm',
                    'color_scheme': 'gold',
                    'font_family': 'Lora, serif',
                    'emoji_theme': '🏖️🌅🎉',
                    'preview_image': 'https://via.placeholder.com/300x400/DAA520/FFFFFF?text=Well+Deserved',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Legacy of Service',
                    'description': 'Honoring years of dedicated professional service',
                    'event_type': 'retirement',
                    'religious_type': 'general',
                    'style': 'professional',
                    'color_scheme': 'navy',
                    'font_family': 'Times New Roman, serif',
                    'emoji_theme': '🏆👔🎖️',
                    'preview_image': 'https://via.placeholder.com/300x400/191970/FFFFFF?text=Legacy+Service',
                    'is_active': True,
                    'usage_count': 0
                },
                
                # Additional Religious Templates
                {
                    'name': 'Hindu Birthday Celebration',
                    'description': 'Traditional Hindu birthday with diyas and rangoli',
                    'event_type': 'birthday',
                    'religious_type': 'hindu',
                    'style': 'traditional',
                    'color_scheme': 'orange',
                    'font_family': 'Noto Sans Devanagari, sans-serif',
                    'emoji_theme': '🪔🌺🎂',
                    'preview_image': 'https://via.placeholder.com/300x400/FF8C00/FFFFFF?text=Hindu+Birthday',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Christian Birthday Blessing',
                    'description': 'Birthday celebration with Christian blessings',
                    'event_type': 'birthday',
                    'religious_type': 'christian',
                    'style': 'blessed',
                    'color_scheme': 'blue',
                    'font_family': 'Georgia, serif',
                    'emoji_theme': '🎂✝️🙏',
                    'preview_image': 'https://via.placeholder.com/300x400/4169E1/FFFFFF?text=Christian+Birthday',
                    'is_active': True,
                    'usage_count': 0
                },
                {
                    'name': 'Church Wedding',
                    'description': 'Beautiful Christian church wedding invitation',
                    'event_type': 'wedding',
                    'religious_type': 'christian',
                    'style': 'classic',
                    'color_scheme': 'white',
                    'font_family': 'Playfair Display, serif',
                    'emoji_theme': '⛪💒🕊️',
                    'preview_image': 'https://via.placeholder.com/300x400/F5F5F5/000000?text=Church+Wedding',
                    'is_active': True,
                    'usage_count': 0
                }
            ]
            
            added_count = 0
            for template_data in templates_to_add:
                # Check if template already exists
                existing_template = Template.query.filter_by(
                    name=template_data['name']
                ).first()
                
                if not existing_template:
                    template = Template(**template_data)
                    db.session.add(template)
                    added_count += 1
                    print(f"✅ Added template: {template_data['name']}")
                else:
                    print(f"⚠️  Template already exists: {template_data['name']}")
            
            db.session.commit()
            print(f"\n🎉 Successfully added {added_count} new templates!")
            
        except Exception as e:
            print(f"❌ Failed to add templates: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    add_more_templates()
