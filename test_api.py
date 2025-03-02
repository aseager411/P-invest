from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://slider_user:secure_password@localhost/slider_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True)
    risk_tolerance = db.Column(db.Integer)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/risk-tolerance', methods=['GET'])
def get_risk():
    user_id = request.args.get('user_id')
    pref = UserPreference.query.filter_by(user_id=user_id).first()
    return jsonify({'risk_tolerance': pref.risk_tolerance if pref else 5})

@app.route('/api/risk-tolerance', methods=['POST'])
def set_risk():
    data = request.json
    pref = UserPreference.query.filter_by(user_id=data['user_id']).first()
    
    if not pref:
        pref = UserPreference(user_id=data['user_id'])
        db.session.add(pref)
    
    pref.risk_tolerance = data['value']
    db.session.commit()
    return jsonify({'status': 'success', 'stored_value': data['value']})

if __name__ == '__main__':
    app.run(debug=True)
