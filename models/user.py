from db import db


class UserModel(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    def add_update_user(self):
        db.session.add(self)
        db.session.commit()
