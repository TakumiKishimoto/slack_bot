from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255), nullable=False)
    full_command = db.Column(db.String(255), nullable=False)

