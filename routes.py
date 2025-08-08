from flask import render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app
from extensions import db
from models import User, OTP, Invitation, Template, EventType, RSVP
from utils import send_otp_email, generate_otp
from datetime import datetime, timedelta
import json
import random
import string
import os

# Helper function to check authentication
def is_authenticated():
    return 'user_id' in session

@app.route('/')
def index():
    if is_authenticated():
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/auth')
def auth():
    if is_authenticated():
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth'))
        
        if User.query.filter_by(mobile=data['mobile']).first():
            flash('Mobile number already registered', 'error')
            return redirect(url_for('auth'))
        
        # Create new user
        user = User(
            name=data['name'],
            mobile=data['mobile'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        
        # Generate and send OTP
        otp_code = generate_otp()
        otp = OTP(
            email=data['email'],
            otp_code=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(otp)
        db.session.commit()
        
        # Send OTP email (in development, this will print to console)
        send_otp_email(data['email'], otp_code)
        
        session['temp_email'] = data['email']
        session['temp_otp'] = otp_code  # For development only
        
        flash(f'OTP sent to your email. For development: {otp_code}', 'success')
        return redirect(url_for('verify_otp'))
        
    except Exception as e:
        app.logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('auth'))

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            if not user.is_verified:
                # Generate and send OTP for verification
                otp_code = generate_otp()
                otp = OTP(
                    email=data['email'],
                    otp_code=otp_code,
                    expires_at=datetime.utcnow() + timedelta(minutes=10)
                )
                db.session.add(otp)
                db.session.commit()
                
                send_otp_email(data['email'], otp_code)
                
                session['temp_email'] = data['email']
                session['temp_otp'] = otp_code  # For development only
                
                flash(f'Please verify your email. OTP sent. For development: {otp_code}', 'info')
                return redirect(url_for('verify_otp'))
            else:
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_email'] = user.email
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth'))
            
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        flash('Login failed. Please try again.', 'error')
        return redirect(url_for('auth'))

@app.route('/verify-otp')
def verify_otp():
    if 'temp_email' not in session:
        flash('Please register or login first', 'error')
        return redirect(url_for('auth'))
    return render_template('auth/verify_otp.html', email=session['temp_email'])

@app.route('/verify-otp', methods=['POST'])
def verify_otp_post():
    try:
        data = request.form
        otp_code = data['otp']
        email = session.get('temp_email')
        
        if not email:
            flash('Session expired. Please try again.', 'error')
            return redirect(url_for('auth'))
        
        # Find valid OTP
        otp = OTP.query.filter_by(
            email=email,
            otp_code=otp_code,
            is_used=False
        ).filter(OTP.expires_at > datetime.utcnow()).first()
        
        if not otp:
            flash('Invalid or expired OTP', 'error')
            return redirect(url_for('verify_otp'))
        
        # Mark OTP as used
        otp.is_used = True
        
        # Mark user as verified
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
        
        db.session.commit()
        
        # Clear temporary session data
        session.pop('temp_email', None)
        session.pop('temp_otp', None)
        
        flash('Email verified successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        app.logger.error(f"OTP verification error: {str(e)}")
        flash('Verification failed. Please try again.', 'error')
        return redirect(url_for('verify_otp'))

@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        flash('Please login to continue', 'error')
        return redirect(url_for('auth'))
    
    user_id = session['user_id']
    user_name = session.get('user_name', 'User')
    user_email = session.get('user_email', '')
    
    invitations = Invitation.query.filter_by(user_id=user_id).order_by(Invitation.created_at.desc()).all()
    
    return render_template('dashboard/dashboard.html', invitations=invitations)

@app.route('/create-invitation')
def create_invitation():
    if not is_authenticated():
        flash('Please login to continue', 'error')
        return redirect(url_for('auth'))
    
    event_types = EventType.query.filter_by(is_active=True).order_by(EventType.sort_order).all()
    return render_template('invitation/create.html', event_types=event_types)

@app.route('/create-invitation', methods=['POST'])
def create_invitation_post():
    print("=== CREATE INVITATION POST CALLED ===")
    print(f"User authenticated: {is_authenticated()}")
    print(f"Session: {session}")
    
    if not is_authenticated():
        flash('Please login to continue', 'error')
        return redirect(url_for('auth'))
    
    try:
        print("Form submitted successfully!")
        print(f"Form data: {request.form}")
        print(f"Files: {request.files}")
        data = request.form
        
        # Handle file uploads
        main_image_filename = None
        gallery_image_filenames = []
        
        # Handle main image upload
        if 'mainImage' in request.files and request.files['mainImage'].filename:
            main_image = request.files['mainImage']
            if main_image and main_image.filename:
                main_image_filename = secure_filename(f"{session['user_id']}_{datetime.utcnow().timestamp()}_{main_image.filename}")
                os.makedirs('uploads', exist_ok=True)
                main_image.save(os.path.join('uploads', main_image_filename))
        
        # Handle gallery images upload
        if 'galleryImages' in request.files:
            gallery_images = request.files.getlist('galleryImages')
            for i, image in enumerate(gallery_images):
                if image and image.filename:
                    filename = secure_filename(f"{session['user_id']}_{datetime.utcnow().timestamp()}_{i}_{image.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    image.save(os.path.join('uploads', filename))
                    gallery_image_filenames.append(filename)
        
        # Filter out any empty filenames from gallery
        gallery_image_filenames = [f for f in gallery_image_filenames if f]
        
        # Handle event-specific file uploads
        bride_photo_filename = None
        groom_photo_filename = None
        couple_photo_filename = None
        birthday_person_photo = None
        graduate_photo = None
        honoree_photo = None
        
        if data['eventType'] == 'wedding':
            # Handle bride photo upload
            if 'bridePhoto' in request.files and request.files['bridePhoto'].filename:
                bride_photo = request.files['bridePhoto']
                if bride_photo and bride_photo.filename:
                    bride_photo_filename = secure_filename(f"{session['user_id']}_bride_{datetime.utcnow().timestamp()}_{bride_photo.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    bride_photo.save(os.path.join('uploads', bride_photo_filename))
            
            # Handle groom photo upload
            if 'groomPhoto' in request.files and request.files['groomPhoto'].filename:
                groom_photo = request.files['groomPhoto']
                if groom_photo and groom_photo.filename:
                    groom_photo_filename = secure_filename(f"{session['user_id']}_groom_{datetime.utcnow().timestamp()}_{groom_photo.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    groom_photo.save(os.path.join('uploads', groom_photo_filename))
            
            # Handle couple photo upload
            if 'couplePhoto' in request.files and request.files['couplePhoto'].filename:
                couple_photo = request.files['couplePhoto']
                if couple_photo and couple_photo.filename:
                    couple_photo_filename = secure_filename(f"{session['user_id']}_couple_{datetime.utcnow().timestamp()}_{couple_photo.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    couple_photo.save(os.path.join('uploads', couple_photo_filename))
        
        elif data['eventType'] == 'birthday':
            # Handle birthday person photo upload
            if 'birthdayPersonPhoto' in request.files and request.files['birthdayPersonPhoto'].filename:
                birthday_photo = request.files['birthdayPersonPhoto']
                if birthday_photo and birthday_photo.filename:
                    birthday_person_photo = secure_filename(f"{session['user_id']}_birthday_{datetime.utcnow().timestamp()}_{birthday_photo.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    birthday_photo.save(os.path.join('uploads', birthday_person_photo))
        
        elif data['eventType'] == 'graduation':
            # Handle graduate photo upload
            if 'graduatePhoto' in request.files and request.files['graduatePhoto'].filename:
                graduate_photo_file = request.files['graduatePhoto']
                if graduate_photo_file and graduate_photo_file.filename:
                    graduate_photo = secure_filename(f"{session['user_id']}_graduate_{datetime.utcnow().timestamp()}_{graduate_photo_file.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    graduate_photo_file.save(os.path.join('uploads', graduate_photo))
        
        elif data['eventType'] == 'retirement':
            # Handle honoree photo upload
            if 'honoreePhoto' in request.files and request.files['honoreePhoto'].filename:
                honoree_photo_file = request.files['honoreePhoto']
                if honoree_photo_file and honoree_photo_file.filename:
                    honoree_photo = secure_filename(f"{session['user_id']}_honoree_{datetime.utcnow().timestamp()}_{honoree_photo_file.filename}")
                    os.makedirs('uploads', exist_ok=True)
                    honoree_photo_file.save(os.path.join('uploads', honoree_photo))
        
        # Store event data in session
        event_data = {
            'eventType': data['eventType'],
            'religiousType': data['religiousType'],
            'familyName': data['familyName'],
            'eventTitle': data['eventTitle'],
            'eventDate': data['eventDate'],
            'eventTime': data['eventTime'],
            'venue': data['venue'],
            'address': data['address'],
            'description': data.get('description', ''),
            'hostName': data['hostName'],
            'contactPhone': data.get('contactPhone', ''),
            'contactEmail': data.get('contactEmail', ''),
            'mainImage': main_image_filename,
            'galleryImages': gallery_image_filenames
        }
        
        # Add event-specific data based on event type
        if data['eventType'] == 'wedding':
            event_data.update({
                'brideName': data.get('brideName', ''),
                'groomName': data.get('groomName', ''),
                'bridePhoto': bride_photo_filename,
                'groomPhoto': groom_photo_filename,
                'couplePhoto': couple_photo_filename,
                'weddingStory': data.get('weddingStory', '')
            })
        elif data['eventType'] == 'birthday':
            event_data.update({
                'birthdayPerson': data.get('birthdayPerson', ''),
                'age': data.get('age', ''),
                'fatherName': data.get('fatherName', ''),
                'motherName': data.get('motherName', ''),
                'birthdayPersonPhoto': birthday_person_photo
            })
        elif data['eventType'] == 'anniversary':
            event_data.update({
                'husbandName': data.get('husbandName', ''),
                'wifeName': data.get('wifeName', ''),
                'years': data.get('years', ''),
                'marriageYear': data.get('marriageYear', ''),
                'firstMilestone': data.get('firstMilestone', ''),
                'secondMilestone': data.get('secondMilestone', '')
            })
        elif data['eventType'] == 'babyshower':
            event_data.update({
                'motherName': data.get('motherName', ''),
                'fatherName': data.get('fatherName', ''),
                'babyName': data.get('babyName', ''),
                'gender': data.get('gender', ''),
                'dueDate': data.get('dueDate', ''),
                'babyGender': data.get('gender', '👶')
            })
        elif data['eventType'] == 'graduation':
            event_data.update({
                'graduateName': data.get('graduateName', ''),
                'degree': data.get('degree', ''),
                'school': data.get('school', ''),
                'major': data.get('major', ''),
                'achievements': data.get('achievements', ''),
                'recognition': data.get('recognition', ''),
                'graduatePhoto': graduate_photo
            })
        elif data['eventType'] == 'retirement':
            event_data.update({
                'honoreeName': data.get('honoreeName', ''),
                'position': data.get('position', ''),
                'company': data.get('company', ''),
                'startYear': data.get('startYear', ''),
                'milestoneYear': data.get('milestoneYear', ''),
                'leadershipYear': data.get('leadershipYear', ''),
                'honoreePhoto': honoree_photo
            })
        
        session['event_data'] = event_data
        
        print("=== REDIRECTING TO SELECT TEMPLATE ===")
        return redirect(url_for('select_template'))
        
    except Exception as e:
        print(f"=== ERROR IN CREATE INVITATION: {str(e)} ===")
        app.logger.error(f"Create invitation error: {str(e)}")
        flash('Failed to create invitation. Please try again.', 'error')
        return redirect(url_for('create_invitation'))

@app.route('/select-template')
def select_template():
    print("=== SELECT TEMPLATE ROUTE CALLED ===")
    print(f"User authenticated: {is_authenticated()}")
    print(f"Event data in session: {'event_data' in session}")
    
    if not is_authenticated() or 'event_data' not in session:
        flash('Please create an invitation first', 'error')
        return redirect(url_for('create_invitation'))
    
    event_type = session['event_data']['eventType']
    religious_type = session['event_data']['religiousType']
    # Get templates for the specific event type and religious type
    templates = Template.query.filter_by(
        event_type=event_type, 
        religious_type=religious_type,
        is_active=True
    ).all()
    
    # Also include general templates for the same event type
    general_templates = Template.query.filter_by(
        event_type=event_type, 
        religious_type='general',
        is_active=True
    ).all()
    
    # Combine and remove duplicates
    all_templates = templates + general_templates
    seen_ids = set()
    unique_templates = []
    for template in all_templates:
        if template.id not in seen_ids:
            seen_ids.add(template.id)
            unique_templates.append(template)
    
    templates = unique_templates
    

    
    return render_template('invitation/select_template.html', 
                         templates=templates, 
                         event_data=session['event_data'])

@app.route('/save-invitation', methods=['POST'])
def save_invitation():
    if not is_authenticated() or 'event_data' not in session:
        flash('Please create an invitation first', 'error')
        return redirect(url_for('create_invitation'))
    
    try:
        data = request.form
        template_id = data['template_id']
        
        # Generate unique share URL
        share_url = ''.join(
            random.choices(string.ascii_letters + string.digits, k=20)
        )
        
        invitation = Invitation(
            user_id=session['user_id'],
            event_type=session['event_data']['eventType'],
            religious_type=session['event_data']['religiousType'],
            family_name=session['event_data']['familyName'],
            main_image=session['event_data'].get('mainImage'),
            gallery_images=json.dumps(session['event_data'].get('galleryImages', [])),
            event_data=json.dumps(session['event_data']),
            template_id=template_id,
            share_url=share_url
        )
        
        db.session.add(invitation)
        db.session.commit()
        
        # Update template usage count
        template = Template.query.get(template_id)
        if template:
            template.usage_count += 1
            db.session.commit()
        
        # Clear session data
        session.pop('event_data', None)
        
        flash('Invitation created successfully!', 'success')
        return redirect(url_for('view_invitation', share_url=invitation.share_url))
        
    except Exception as e:
        app.logger.error(f"Save invitation error: {str(e)}")
        flash('Failed to save invitation. Please try again.', 'error')
        return redirect(url_for('select_template'))

@app.route('/invitation/<share_url>')
def view_invitation(share_url):
    invitation = Invitation.query.filter_by(share_url=share_url, is_active=True).first_or_404()
    print("Raw gallery_images:", invitation.gallery_images)
    try:
        gallery_list = json.loads(invitation.gallery_images)
        print("Parsed gallery_list:", gallery_list)
    except Exception as e:
        print("Error parsing gallery_images:", e)
    # Increment view count
    invitation.view_count += 1
    db.session.commit()
    event_data = json.loads(invitation.event_data)
    template = Template.query.get(invitation.template_id)
    
    # Debug template selection
    print(f"Debug: Template ID: {invitation.template_id}")
    print(f"Debug: Template: {template}")
    if template:
        print(f"Debug: Template event_type: {template.event_type}")
        print(f"Debug: Template religious_type: {template.religious_type}")
    
    # Check if there's a custom template file for this template
    template_file = None
    
    # First check if there's a specific template based on event type and religious type
    if template and template.event_type == 'wedding' and template.religious_type:
        if template.religious_type == 'hindu':
            template_file = 'invitation/templates/wedding_hindu_traditional.html'
        elif template.religious_type == 'muslim':
            template_file = 'invitation/templates/wedding_muslim_elegant.html'
    
    # If no specific religious template, use event type mapping
    if not template_file:
        event_type_to_template = {
            'birthday': 'invitation/templates/birthday_fun_colorful.html',
            'wedding': 'invitation/templates/wedding_elegant.html',
            'anniversary': 'invitation/templates/anniversary_golden_elegant.html',
            'babyshower': 'invitation/templates/babyshower_sweet_pink.html',
            'graduation': 'invitation/templates/graduation_success_modern.html',
            'retirement': 'invitation/templates/retirement_golden_classic.html',
        }
        if template and template.event_type in event_type_to_template:
            template_file = event_type_to_template[template.event_type]
    
    # Fallback to default template
    if not template_file:
        template_file = 'invitation/view.html'
    
    print(f"Debug: Final template_file: {template_file}")
    
    return render_template(template_file,
                         event_data=event_data,
                         template=template,
                         invitation=invitation)

@app.route('/rsvp/<share_url>', methods=['POST'])
def rsvp_response(share_url):
    invitation = Invitation.query.filter_by(share_url=share_url, is_active=True).first_or_404()
    
    try:
        data = request.form
        
        rsvp = RSVP(
            invitation_id=invitation.id,
            guest_name=data['guest_name'],
            guest_email=data.get('guest_email'),
            guest_phone=data.get('guest_phone'),
            response=data['response'],
            guest_count=int(data.get('guest_count', 1)),
            message=data.get('message')
        )
        
        db.session.add(rsvp)
        db.session.commit()
        
        # Mark RSVP as submitted in session
        session[f'rsvp_submitted_{share_url}'] = True
        
        flash('RSVP submitted successfully!', 'success')
        return redirect(url_for('view_invitation', share_url=share_url))
        
    except Exception as e:
        app.logger.error(f"RSVP error: {str(e)}")
        flash('Failed to submit RSVP. Please try again.', 'error')
        return redirect(url_for('view_invitation', share_url=share_url))

@app.route('/manage-invitation/<int:invitation_id>')
def view_invitation_manage(invitation_id):
    if not is_authenticated():
        flash('Please login to continue', 'error')
        return redirect(url_for('auth'))
    
    invitation = Invitation.query.filter_by(id=invitation_id, user_id=session['user_id']).first_or_404()
    event_data = json.loads(invitation.event_data)
    template = Template.query.get(invitation.template_id)
    rsvps = RSVP.query.filter_by(invitation_id=invitation.id).order_by(RSVP.responded_at.desc()).all()
    
    # Calculate RSVP statistics
    rsvp_stats = {
        'total': len(rsvps),
        'yes': len([r for r in rsvps if r.response == 'yes']),
        'no': len([r for r in rsvps if r.response == 'no']),
        'maybe': len([r for r in rsvps if r.response == 'maybe']),
        'total_guests': sum([r.guest_count for r in rsvps if r.response == 'yes'])
    }
    
    return render_template('invitation/manage.html',
                         invitation=invitation,
                         event_data=event_data,
                         template=template,
                         rsvps=rsvps,
                         rsvp_stats=rsvp_stats)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/debug-session')
def debug_session():
    """Debug route to check session data"""
    if not is_authenticated():
        return "Not authenticated"
    
    debug_info = {
        'user_id': session.get('user_id'),
        'user_name': session.get('user_name'),
        'user_email': session.get('user_email'),
        'session_keys': list(session.keys())
    }
    
    # Get user from database
    user = User.query.get(session.get('user_id'))
    if user:
        debug_info['db_user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_verified': user.is_verified
        }
    
    return f"<pre>{debug_info}</pre>"

@app.route('/test-form', methods=['GET', 'POST'])
def test_form():
    if request.method == 'POST':
        print("Test form submitted!")
        print(f"Form data: {request.form}")
        print(f"Files: {request.files}")
        return jsonify({'success': True, 'data': dict(request.form)})
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Form</title>
    </head>
    <body>
        <h2>Test Form</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="test_field" value="test_value" required><br><br>
            <input type="file" name="test_file"><br><br>
            <button type="submit">Test Submit</button>
        </form>
        <br>
        <a href="/create-invitation">Go to Create Invitation</a>
    </body>
    </html>
    '''

@app.route('/test-email')
def test_email():
    """Debug route to test email sending"""
    from utils import send_otp_email
    import random
    
    test_otp = str(random.randint(100000, 999999))
    test_email = "jmadhan087@mail.com"  # Use your email for testing
    
    print(f"Testing email send to: {test_email}")
    print(f"Test OTP: {test_otp}")
    
    try:
        result = send_otp_email(test_email, test_otp)
        return f"Email test result: {result}<br>Check console logs for details.<br>Test OTP was: {test_otp}"
    except Exception as e:
        return f"Email test failed: {str(e)}<br>Check console logs for details."

@app.route('/verify-direct/<email>/<otp>')
def verify_direct(email, otp):
    """Direct verification route for testing when email doesn't arrive"""
    try:
        # Check if user exists in session
        if 'pending_otp' in session and session.get('pending_email') == email:
            stored_otp = session['pending_otp']
            if stored_otp == otp:
                # Mark user as verified
                user = User.query.filter_by(email=email).first()
                if user:
                    user.is_verified = True
                    db.session.commit()
                    
                    # Clear session data
                    session.pop('pending_otp', None)
                    session.pop('pending_email', None)
                    session.pop('pending_user_id', None)
                    
                    # Log user in
                    session['user_id'] = user.id
                    session['is_authenticated'] = True
                    
                    flash('Email verified successfully! You are now logged in.', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    return "User not found", 404
            else:
                return f"Invalid OTP. Expected: {stored_otp}, Got: {otp}", 400
        else:
            return "No pending verification found", 400
            
    except Exception as e:
        return f"Verification error: {str(e)}", 500
