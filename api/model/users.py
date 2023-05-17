from ..utils import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"<user {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
