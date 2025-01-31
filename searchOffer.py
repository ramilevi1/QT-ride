from flask import Flask, render_template, url_for, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from app import db 

app = Flask(__name__)
# Databse path (relative path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ride.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# This is the database 
class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('Search_Offer/search_offer_home.html')

@app.route('/offer_ride', methods=['POST','GET'])
def offer_ride():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validate data
            required_fields = ['origin', 'destination', 'date', 'time', 'seats_available']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing field: {field}'}), 400

            # Create a new ride instance
            new_ride = Ride(
                origin=data['origin'],
                destination=data['destination'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(data['time'], '%H:%M').time(),
                seats_available=int(data['seats_available']),
                price=float(data['price']) if 'price' in data and data['price'] else None
            )

            db.session.add(new_ride)
            db.session.commit()
            return jsonify({'message': 'Ride offered successfully!'}), 201

        except Exception as e:
            print(f"Error: {e}")  # Debugging
            return jsonify({'error': 'Failed to add ride to the database'}), 500

    return render_template('Search_Offer/offer_ride.html')

@app.route('/search_ride', methods=['GET', 'POST'])
def search_ride():
    rides = Ride.query.order_by(Ride.date_created).all()
    return render_template('Search_Offer/search_ride.html', rides=rides)


# @app.route('/offer_ride', methods=['POST'])
# def offer_ride():
#     data = request.get_json()

#     # Validate input
#     required_fields = ['origin', 'destination', 'date', 'time', 'seats']
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return jsonify({'error': f'Missing field: {field}'}), 400

#     # Add ride to database or in-memory list
#     ride = {
#         'origin': data['origin'],
#         'destination': data['destination'],
#         'date': data['date'],
#         'time': data['time'],
#         'seats': data['seats'], 
#         'price': data.get('price')  # Optional field
#     }
#     rides.append(ride)

#     return jsonify({'message': 'Ride offered successfully!', 'ride': ride}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)