from flask import Flask, request, jsonify  # Import necessary modules from Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database management

app = Flask(__name__)  # Initialize the Flask application

# Configure the database connection URI for a PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://slider_user:secure_password@localhost/slider_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to improve performance

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define a database model for storing user preferences
class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, auto-incremented
    user_id = db.Column(db.String(50), unique=True)  # Unique identifier for the user
    risk_tolerance = db.Column(db.Integer)  # Integer field for risk tolerance level

# Ensure tables are created before the first request to the API
@app.before_first_request
def create_tables():
    db.create_all()

# API endpoint to retrieve a user's risk tolerance
@app.route('/api/risk-tolerance', methods=['GET'])
def get_risk():
    user_id = request.args.get('user_id')  # Get the user_id from query parameters
    pref = UserPreference.query.filter_by(user_id=user_id).first()  # Fetch the user preference from the database
    return jsonify({'risk_tolerance': pref.risk_tolerance if pref else 5})  # Return stored value or default to 5

# API endpoint to set a user's risk tolerance
@app.route('/api/risk-tolerance', methods=['POST'])
def set_risk():
    data = request.json  # Parse JSON payload from the request
    pref = UserPreference.query.filter_by(user_id=data['user_id']).first()  # Fetch existing record if it exists
    
    if not pref:
        pref = UserPreference(user_id=data['user_id'])  # Create a new entry if none exists
        db.session.add(pref)  # Add new entry to the session
    
    pref.risk_tolerance = data['value']  # Update the risk tolerance value
    db.session.commit()  # Commit the changes to the database
    
    return jsonify({'status': 'success', 'stored_value': data['value']})  # Return confirmation response

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
