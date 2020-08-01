from system import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(300), nullable=False)
    short_url = db.Column(db.String(6), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Url('{self.long_url}', '{self.short_url}')"