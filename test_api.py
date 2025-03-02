from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://slider_user:secure_password@localhost/slider_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RiskTolerance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/risk-tolerance', methods=['GET'])
def get_risk():
    entry = RiskTolerance.query.first()
    return jsonify({'risk_tolerance': entry.value if entry else 5})

@app.route('/api/risk-tolerance', methods=['POST'])
def set_risk():
    data = request.json
    entry = RiskTolerance.query.first()
    
    if not entry:
        entry = RiskTolerance(value=data['value'])
        db.session.add(entry)
    else:
        entry.value = data['value']
    
    db.session.commit()
    return jsonify({'status': 'success', 'stored_value': data['value']})

if __name__ == '__main__':
    app.run(debug=True)
