from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User, UserSession, UserSet, UserRep, ProgramTemplate
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token
from .utils import factory
import json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403


@app.route("/api/get_workout_for_date", methods=["POST"])
@requires_auth
def get_workout_for_date():
    incoming = request.get_json()
    dates = incoming["dates"]
    workouts = [UserSession.query.filter_by(date=date, user_id=g.current_user["id"]).first() for date in dates]


@app.route("/api/create_workouts_for_user", methods=["POST"])
@requires_auth
def create_workouts():
    incoming = request.get_json()

    template = ProgramTemplate.query.filter_by(id=incoming["prog"]).first()
    prog_id = template.id
    template = json.loads(template.program)

    gen = factory.get_next(incoming["weight"], template["weights"], template["times"], template["freqs"])

    new_sessions = [UserSession(
        user_id=g.current_user["id"],
        date=date,
        grip=incoming["grip"],
        note="",
        program=prog_id,
        sets=[UserSet(
            rest = set_["rest"],
            ordinal = set_["ordinal"],
            completed = False,
            effort_level = -1,
            reps = [ UserRep(
                time_on = rep["time_on"],
                time_off= rep["time_off"],
                weight=rep["weight"],
                ordinal=rep["ordinal"]
            ) for rep in set_["reps"] ]
        ) for set_ in (next(gen))["sets"]]
    ) for date in incoming["dates"]]

    db.session.add_all(new_sessions)
    db.session.commit()
    new_sessions = [{
        "user_id":session.user_id,
        "date":session.date,
        "grip":session.grip,
        "note":session.note,
        "program":session.program,
        "sets":[{
            "rest": set_.rest,
            "ordinal": set_.ordinal,
            "completed": set_.completed,
            "effort_level": set_.effort_level,
            "reps": [{
                "time_on": rep.time_on,
                "time_off": rep.time_off,
                "weight":rep.weight,
                "ordinal":rep.ordinal
            } for rep in set_.reps]
        } for set_ in session.sets]
    } for session in new_sessions]

    return jsonify(sessions=new_sessions)
