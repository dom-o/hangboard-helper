from flask_testing import TestCase
from application.app import app, db
from application.models import User, ProgramTemplate
import os
from setup import basedir
import json


class BaseTestConfig(TestCase):
    default_user = {
        "email": "default@gmail.com",
        "password": "something2",
        "imperial": True,
        "bodyweight": 180
    }

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.drop_all()
        db.create_all()
        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.default_user),
                content_type='application/json'
        )

        self.token = json.loads(res.data.decode("utf-8"))["token"]

        test_program = ProgramTemplate(name="test_program",
            program=json.dumps({
                "weights": {
                    "pre": "0.9*X",
                    "session": ["X+0"],
                    "set":[["0.65*X", "0.75*X", "0.85*X"],
                        ["0.7*X", "0.8*X", "0.9*X"],
                        ["0.75*X", "0.85*X", "0.95*X"],
                        ["0.4*X", "0.5*X", "0.6*X"]],
                    "rep": [["X+0"]]
                },
                "times": {
                    "session": [],
                    "set":[[180, 150]],
                    "rep":[[[10,6,2], [5,3,1]], [[6,2], [3,1]], [[2],[1]]]
                },
                "freqs": {
                    "session": [2, 2, 2, 1],
                    "set":[3],
                    "rep":[3,2,2]
                }
            })
        )
        db.session.add(test_program)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
