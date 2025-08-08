# EventCraft Pro

## Overview

EventCraft Pro is a digital event invitation platform built with Flask that allows users to create, customize, and manage event invitations online. The application supports multiple event types (weddings, birthdays, baby showers, graduations, anniversaries, and retirement parties) with professional templates and RSVP tracking functionality. Users can register accounts, verify their email through OTP, create invitations using pre-designed templates, and share them via unique URLs while tracking views and responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework & Application Structure
- **Flask-based architecture** with modular design using blueprints pattern
- **Template-driven UI** using Jinja2 templating engine with Bootstrap 5 for responsive design
- **SQLAlchemy ORM** for database operations with declarative base model approach
- **Session-based authentication** using Flask's built-in session management

### Database Design
- **SQLite default with PostgreSQL support** - Uses SQLite for development with environment variable configuration for production databases
- **User management system** with email verification via OTP (One-Time Password)
- **Event type categorization** with customizable templates and color schemes
- **RSVP tracking system** to monitor invitation responses and view counts
- **Invitation sharing** through unique shareable URLs

### Authentication & Security
- **Email-based OTP verification** for user registration with 10-minute expiration
- **Password hashing** using Werkzeug's security utilities
- **Session management** for maintaining user login state
- **CORS headers** configured for cross-origin requests

### File Management
- **Upload handling** with 16MB file size limit for invitation assets
- **Static file serving** for CSS, JavaScript, and uploaded content
- **Directory structure** with organized templates and static assets

### Frontend Architecture
- **Bootstrap 5 responsive framework** for modern UI components
- **Font Awesome icons** for consistent iconography
- **Custom CSS** with CSS variables for theme consistency
- **Progressive JavaScript enhancement** with form validation and loading states

### Email Integration
- **SMTP configuration** ready for production email sending
- **Development mode** with console output for OTP codes
- **Template-based email** system for user communications

## External Dependencies

### Core Framework Dependencies
- **Flask** - Web application framework
- **Flask-SQLAlchemy** - Database ORM integration
- **Werkzeug** - WSGI utilities and security functions

### Frontend Libraries
- **Bootstrap 5** - CSS framework via CDN
- **Font Awesome** - Icon library via CDN
- **Custom JavaScript** - Form validation and UI enhancements

### Database Support
- **SQLite** - Default development database
- **PostgreSQL** - Production database support via DATABASE_URL environment variable

### Email Services
- **SMTP integration** - Configurable email server for OTP delivery
- **Gmail SMTP** - Default configuration with environment variable overrides

### Environment Configuration
- **Development/Production modes** - Environment-based configuration
- **File upload management** - Configurable upload directories and size limits
- **Database URL configuration** - Flexible database connection strings