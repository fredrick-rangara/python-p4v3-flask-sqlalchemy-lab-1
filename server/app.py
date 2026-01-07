# server/app.py
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Task #3: Get an earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query for the specific earthquake
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake:
        # Convert model instance to dictionary and return 200
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        # Return the specific error message and 404 status
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)

# Task #4: Filter by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Filter quakes >= magnitude
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Format for the JSON response
    response_dict = {
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }
    
    return make_response(jsonify(response_dict), 200)