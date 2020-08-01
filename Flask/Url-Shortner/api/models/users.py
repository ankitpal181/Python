from system import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    url_count = db.Column(db.Integer, nullable=True)
    urls = db.relationship('Url', backref='creator')

    def __repr__(self):
        return f"Url('{self.email}')"