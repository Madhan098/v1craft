#!/usr/bin/env python3
"""
Script to update the database with new templates
"""

import os
import sys
from app import app, db
from models import Template

def update_templates():
    """Update the database with new templates"""
    
    with app.app_context():
        # New templates to add
        new_templates = [
            {
                'name': 'Traditional Hindu Wedding',
                'description': 'Traditional Hindu wedding with sacred symbols and cultural elements',
                'event_type': 'wedding',
                'religious_type': 'hindu',
                'style': 'traditional',
                'color_scheme': 'orange',
                'font_family': 'Playfair Display, serif',
                'emoji_theme': '🕉️💒🌺',
                'preview_image': 'https://via.placeholder.com/300x400/FF6B35/FFFFFF?text=Hindu+Wedding'
            },
            {
                'name': 'Elegant Muslim Wedding',
                'description': 'Beautiful Islamic wedding with elegant design and cultural elements',
                'event_type': 'wedding',
                'religious_type': 'muslim',
                'style': 'elegant',
                'color_scheme': 'green',
                'font_family': 'Playfair Display, serif',
                'emoji_theme': '☪️🕌💚',
                'preview_image': 'https://via.placeholder.com/300x400/228B22/FFFFFF?text=Muslim+Wedding'
            },
            {
                'name': 'Fun & Colorful Birthday',
                'description': 'Vibrant and playful birthday invitation with floating balloons',
                'event_type': 'birthday',
                'religious_type': 'general',
                'style': 'fun',
                'color_scheme': 'pink',
                'font_family': 'Fredoka One, cursive',
                'emoji_theme': '🎂🎉🎈',
                'preview_image': 'https://via.placeholder.com/300x400/FF69B4/FFFFFF?text=Fun+Birthday'
            },
            {
                'name': 'Golden Elegant Anniversary',
                'description': 'Elegant anniversary celebration with timeline and golden design',
                'event_type': 'anniversary',
                'religious_type': 'general',
                'style': 'elegant',
                'color_scheme': 'gold',
                'font_family': 'Playfair Display, serif',
                'emoji_theme': '💑💍💎',
                'preview_image': 'https://via.placeholder.com/300x400/FFD700/000000?text=Golden+Anniversary'
            },
            {
                'name': 'Sweet Pink Baby Shower',
                'description': 'Adorable baby shower invitation with floating baby elements',
                'event_type': 'babyshower',
                'religious_type': 'general',
                'style': 'cute',
                'color_scheme': 'pink',
                'font_family': 'Dancing Script, cursive',
                'emoji_theme': '👶🍼🧸',
                'preview_image': 'https://via.placeholder.com/300x400/FFB6C1/000000?text=Sweet+Baby+Shower'
            },
            {
                'name': 'Modern Graduation Success',
                'description': 'Modern graduation celebration with academic achievements',
                'event_type': 'graduation',
                'religious_type': 'general',
                'style': 'modern',
                'color_scheme': 'blue',
                'font_family': 'Playfair Display, serif',
                'emoji_theme': '🎓📚🏆',
                'preview_image': 'https://via.placeholder.com/300x400/4169E1/FFFFFF?text=Graduation+Success'
            },
            {
                'name': 'Golden Classic Retirement',
                'description': 'Classic retirement celebration with career timeline',
                'event_type': 'retirement',
                'religious_type': 'general',
                'style': 'classic',
                'color_scheme': 'gold',
                'font_family': 'Playfair Display, serif',
                'emoji_theme': '👑🏆⭐',
                'preview_image': 'https://via.placeholder.com/300x400/FFD700/000000?text=Retirement+Celebration'
            }
        ]
        
        # Add new templates
        for template_data in new_templates:
            existing_template = Template.query.filter_by(name=template_data['name']).first()
            if not existing_template:
                template = Template(**template_data)
                db.session.add(template)
                print(f"Added template: {template_data['name']}")
            else:
                print(f"Template already exists: {template_data['name']}")
        
        # Commit changes
        db.session.commit()
        print("Database updated successfully!")

if __name__ == '__main__':
    update_templates()
