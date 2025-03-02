# Import core Flask modules for web framework functionality
from flask import Flask, request, jsonify
# Import SQLAlchemy for ORM-based database management
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application instance
app = Flask(__name__)

# Configure database connection using PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://slider_user:secure_password@localhost/slider_db'
    
# Disable Flask-SQLAlchemy modification tracking to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection instance
db = SQLAlchemy(app)

# Define database model for storing risk tolerance values
class RiskTolerance(db.Model):
    # Primary key column (auto-incrementing integer)
    id = db.Column(db.Integer, primary_key=True)
    # Integer column to store the risk tolerance value (1-10)
    value = db.Column(db.Integer)

# Create database tables before first request (if they don't exist)
@app.before_first_request
def create_tables():
    # Creates all defined models as database tables
    db.create_all()

# GET endpoint to retrieve current risk tolerance value
@app.route('/api/risk-tolerance', methods=['GET'])
def get_risk():
    # Fetch first record from RiskTolerance table
    entry = RiskTolerance.query.first()
    # Return 5 as default value if no records exist
    return jsonify({'risk_tolerance': entry.value if entry else 5})

# POST endpoint to update risk tolerance value
@app.route('/api/risk-tolerance', methods=['POST'])
def set_risk():
    # Parse JSON data from request body
    data = request.json
    
    # Check for existing record
    entry = RiskTolerance.query.first()
    
    if not entry:
        # Create new record if none exists
        entry = RiskTolerance(value=data['value'])
        db.session.add(entry)
    else:
        # Update existing record value
        entry.value = data['value']
    
    # Commit transaction to database
    db.session.commit()
    # Return success response with stored value
    return jsonify({'status': 'success', 'stored_value': data['value']})

# Main entry point for running the application
if __name__ == '__main__':
    # Start Flask development server with debug mode enabled
    app.run(debug=True)
