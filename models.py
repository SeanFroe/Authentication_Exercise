from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()



class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                   primary_key=True,
                   unique=True,
                   nullable=False)
    password = db.Column(db.Text(),
                     nullable=False)
    email = db.Column(db.String(50), 
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    feedback = db.relationship("Feedback", backref='user', cascade="all,delete")

    # start of covenience class methods

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        print(f"Hashed password: {hashed_utf8}")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        
        Return user if valid; else return False
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )

def connect_db(app):
    """Connect this database to provide Flask app"""

    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()