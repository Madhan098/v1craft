import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(email, otp_code):
    """Send OTP via email using Gmail SMTP"""
    
    try:
        # Gmail SMTP configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'jmadhanplacement@gmail.com'
        smtp_password = 'tsvxkjddyiqiehxj'
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"EventCraft Pro <{smtp_username}>"
        msg['To'] = email
        msg['Subject'] = "EventCraft Pro - Email Verification OTP"
        msg['Reply-To'] = smtp_username
        
        # Email body with both HTML and plain text
        html_body = f'''
        <html>
        <body>
            <h2 style="color: #1a237e;">EventCraft Pro - Email Verification</h2>
            <p>Hello,</p>
            <p>Your OTP for EventCraft Pro email verification is:</p>
            <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                <h1 style="color: #1a237e; font-size: 36px; margin: 0; letter-spacing: 5px;">{otp_code}</h1>
            </div>
            <p><strong>This OTP will expire in 10 minutes.</strong></p>
            <p>If you didn't request this verification, please ignore this email.</p>
            <hr>
            <p style="color: #666; font-size: 12px;">EventCraft Pro - Digital Event Invitations</p>
        </body>
        </html>
        '''
        
        plain_body = f'''
EventCraft Pro - Email Verification

Hello,

Your OTP for EventCraft Pro email verification is: {otp_code}

This OTP will expire in 10 minutes.

If you didn't request this verification, please ignore this email.

---
EventCraft Pro - Digital Event Invitations
        '''
        
        # Attach both plain text and HTML versions
        msg.attach(MIMEText(plain_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email with detailed logging
        print(f"Attempting to send email to: {email}")
        print(f"Using SMTP server: {smtp_server}:{smtp_port}")
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        print("STARTTLS enabled")
        
        server.login(smtp_username, smtp_password)
        print("SMTP login successful")
        
        text = msg.as_string()
        result = server.sendmail(smtp_username, email, text)
        server.quit()
        
        print(f"SMTP sendmail result: {result}")
        print(f"OTP email sent successfully to {email}")
        
        # Additional verification
        if not result:
            print("Email sent without errors")
        else:
            print(f"Email sent with some delivery issues: {result}")
            
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        
        # Try with different approach - simple message
        try:
            print("Attempting simple email approach...")
            
            # Simple message without multipart
            simple_msg = MIMEText(f"""
EventCraft Pro - Email Verification

Your OTP code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.
            """)
            
            simple_msg['Subject'] = "EventCraft Pro - OTP Verification"
            simple_msg['From'] = 'jmadhanplacement@gmail.com'
            simple_msg['To'] = email
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('jmadhanplacement@gmail.com', 'tsvxkjddyiqiehxj')
            server.send_message(simple_msg)
            server.quit()
            
            print(f"Simple OTP email sent successfully to {email}")
            return True
            
        except Exception as e2:
            print(f"Simple email also failed: {str(e2)}")
            
        # Fallback to console output for debugging
        print(f"=== OTP EMAIL (FALLBACK) ===")
        print(f"To: {email}")
        print(f"OTP Code: {otp_code}")
        print(f"================")
        
        # Provide troubleshooting suggestions
        print("TROUBLESHOOTING SUGGESTIONS:")
        print("1. Check if Gmail account has 2-factor authentication enabled")
        print("2. Verify the app password is correct and hasn't expired")
        print("3. Check spam/junk folder for the email")
        print("4. Try with a different email address")
        
        return False

def format_date(date_str):
    """Format date string for display"""
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def format_time(time_str):
    """Format time string for display"""
    from datetime import datetime
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')
    except:
        return time_str
