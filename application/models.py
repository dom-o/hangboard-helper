from index import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.Binary(60), nullable=False)
    bodyweight = db.Column(db.Integer())
    one_rep_max = db.relationship("OneRepMax")
    imperial = db.Column(db.Boolean())
    sessions = db.relationship("UserSession", lazy="dynamic")

    def __init__(self, email, password, imperial=True, bodyweight=-1):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)
        self.imperial = imperial
        self.bodyweight = bodyweight

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None


class UserSession(db.Model):
    __tablename__ = "user_session"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    date = db.Column(db.Date())
    sets = db.relationship("UserSet")
    note = db.Column(db.Text())
    grip = db.Column(db.String(255))
    program = db.Column(db.Integer(), db.ForeignKey("program_template.id"))


class UserSet(db.Model):
    __tablename__ = "user_set"
    id = db.Column(db.Integer(), primary_key=True)
    workout_id = db.Column(db.Integer(), db.ForeignKey("user_session.id"))
    reps = db.relationship("UserRep")
    rest = db.Column(db.Integer())
    ordinal = db.Column(db.Integer())
    completed = db.Column(db.Boolean())
    effort_level = db.Column(db.Integer())

class UserRep(db.Model):
    __tablename__ = "user_rep"
    id = db.Column(db.Integer(), primary_key=True)
    set_id = db.Column(db.Integer(), db.ForeignKey("user_set.id"))
    time_on = db.Column(db.Integer())
    time_off = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    ordinal = db.Column(db.Integer())

class OneRepMax(db.Model):
    __tablename__ = "one_rep_max"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    grip = db.Column(db.String())
    left_hand = db.Column(db.Integer())
    right_hand = db.Column(db.Integer())
    combined = db.Column(db.Integer())


class ProgramTemplate(db.Model):
    __tablename__ = "program_template"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    program = db.Column(JSON)
