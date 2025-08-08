import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.environ.get("SESSION_SECRET", "eventcraft-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    # Default to SQLite for development
    db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database'))
    os.makedirs(db_dir, exist_ok=True)
    db_file = os.path.join(db_dir, 'eventcraft.db')
    database_url = f'sqlite:///{db_file}'

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the app with the extension
db.init_app(app)

# Add custom Jinja2 filters
@app.template_filter('fromjson')
def fromjson_filter(value):
    if value:
        return json.loads(value)
    return {}

@app.template_filter('from_json')
def from_json_filter(value):
    if value:
        return json.loads(value)
    return {}

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Import models and routes after app initialization
with app.app_context():
    import models  # noqa: F401
    import routes  # noqa: F401
    db.create_all()

    # Initialize sample data if tables are empty
    from models import init_sample_data
    if not models.EventType.query.first():
        init_sample_data()