import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import time

app = Flask(__name__)

# It configures db connection using env variable from compose
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo of visitor table
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Visitor {self.name}>'

# Function to initialize db
def init_db():
    retries = 5
    while retries > 0:
        try:
            # db.create_all() creates tables based on the defined models
            db.create_all()
            print("DB connected and tables created!")
            return
        except Exception as e:
            print("Error connecting to db, trying again...", e)
            retries -= 1
            time.sleep(5)
    print("Unable to connect to database.")

@app.route("/api")
def api_visitors():
    # Add new visitor with random ID
    visitor_count = Visitor.query.count() + 1
    new_visitor = Visitor(name=f'Visitor_{visitor_count}')
    db.session.add(new_visitor)
    db.session.commit()

    # Returns all visitors
    visitors = Visitor.query.all()
    visitor_list = [v.name for v in visitors]
    
    return jsonify(message="List of visitors", visitors=visitor_list)

@app.route("/health")
def health_check():
    try:
        # tries to run a query to check connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify(status="OK"), 200
    except Exception as e:
        # returns error 503 (service unavailable), if it fails
        return jsonify(status="error", details=str(e)), 503

@app.before_request
def before_request():
    if not hasattr(app, "_db_initialized"):
        try:
            init_db()
            app._db_initialized = True
        except Exception as e:
            print("Database not ready yet:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)