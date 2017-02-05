from testing_config import BaseTestConfig
from application.models import User, UserSession, ProgramTemplate
import json, calendar
from datetime import datetime
from email.utils import format_datetime
from application.utils import auth

class TestAPI(BaseTestConfig):
    some_user = {
        "email": "one@gmail.com",
        "password": "something1",
        "imperial": True,
        "bodyweight": 150
    }
    maxDiff = None

    def test_get_spa_from_index(self):
        result = self.app.get("/")
        self.assertIn('<html>', result.data.decode("utf-8"))

    def test_create_new_user(self):
        self.assertIsNone(User.query.filter_by(
                email=self.some_user["email"]
        ).first())

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data.decode("utf-8"))["token"])
        self.assertEqual(User.query.filter_by(email=self.some_user["email"]).first().email, self.some_user["email"])

        res2 = self.app.post(
                "/api/create_user",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )

        self.assertEqual(res2.status_code, 409)

    def test_get_token_and_verify_token(self):
        res = self.app.post(
                "/api/get_token",
                data=json.dumps(self.default_user),
                content_type='application/json'
        )

        token = json.loads(res.data.decode("utf-8"))["token"]
        self.assertTrue(auth.verify_token(token))
        self.assertEqual(res.status_code, 200)

        res2 = self.app.post(
                "/api/is_token_valid",
                data=json.dumps({"token": token}),
                content_type='application/json'
        )

        self.assertTrue(json.loads(res2.data.decode("utf-8")), ["token_is_valid"])

        res3 = self.app.post(
                "/api/is_token_valid",
                data=json.dumps({"token": token + "something-else"}),
                content_type='application/json'
        )

        self.assertEqual(res3.status_code, 403)

        res4 = self.app.post(
                "/api/get_token",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )

        self.assertEqual(res4.status_code, 403)

    def test_protected_route(self):
        headers = {
            'Authorization': self.token,
        }

        bad_headers = {
            'Authorization': self.token + "bad",
        }

        response = self.app.get('/api/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        response2 = self.app.get('/api/user')
        self.assertEqual(response2.status_code, 401)
        response3 = self.app.get('/api/user', headers=bad_headers)
        self.assertEqual(response3.status_code, 401)


    def test_generate_workouts_for_user(self):
        headers = {
            "Authorization": self.token
        }
        dates = [format_datetime(datetime(2017, 1, x), usegmt=False) for x in range(1,6)]
        prog_id = ProgramTemplate.query.filter_by(name="test_program").first().id
        response = self.app.post(
            "/api/create_workouts_for_user",
            data=json.dumps({
                "dates": [date for date in dates],
                "prog": prog_id,
                "weight": 111.111111111111111111111111111111111,
                "grip": "half crimp",
            }),
            headers=headers,
            content_type="application/json"
        )

        #get workouts put into database here
        db_sessions = [UserSession.query.filter_by(date=date).first() for date in dates]
        db_sessions = [{
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
        } for session in db_sessions]

        #compare return workouts with workouts from databases with master workouts here
        user_id = json.loads(self.app.get('/api/user', headers=headers).data.decode("utf-8"))["result"]["id"]
        expected_sessions=[{
            "user_id": user_id, "date": dates[0], "grip": "half crimp", "note": "", "program": prog_id,
            'sets': [{
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 65
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 65
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 65
                }], 'rest': 180, 'ordinal': 0, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 75
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 75
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 75
                }],
                'rest': 150, 'ordinal': 1, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 85
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 85
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 85
                }],
                'rest': 180, 'ordinal': 2, "completed": False, "effort_level": -1
            }]
        }, {
            "user_id": user_id, "date": dates[1], "grip": "half crimp", "note": "", "program": prog_id,
            'sets': [{
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 65
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 65
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 65
                }],
                'rest': 180, 'ordinal': 0, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 75
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 75
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 75
                }],
                'rest': 150, 'ordinal': 1, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 85
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 85
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 85
                }],
                'rest': 180, 'ordinal': 2, "completed": False, "effort_level": -1
            }]
        }, {
            "user_id": user_id, "date": dates[2], "grip": "half crimp", "note": "", "program": prog_id,
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 70
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 70
                }],
                'rest': 180, 'ordinal': 0, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 80
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 80
                }],
                'rest': 150, 'ordinal': 1, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 90
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 90
                }],
                'rest': 180, 'ordinal': 2, "completed": False, "effort_level": -1
            }]
        }, {
            "user_id": user_id, "date": dates[3], "grip": "half crimp", "note": "", "program": prog_id,
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 70
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 70
                }],
                'rest': 180, 'ordinal': 0, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 80
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 80
                }],
                'rest': 150, 'ordinal': 1, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 90
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 90
                }],
                'rest': 180, 'ordinal': 2, "completed": False, "effort_level": -1
            }]
        }, {
            "user_id": user_id, "date": dates[4], "grip": "half crimp", "note": "", "program": prog_id,
            'sets': [{
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 75
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 75
                }],
                'rest': 180, 'ordinal': 0, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 85
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 85
                }],
                'rest': 150, 'ordinal': 1, "completed": False, "effort_level": -1
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 95
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 95
                }],
                'rest': 180, 'ordinal': 2, "completed": False, "effort_level": -1
            }]
        }]
        print(dates[0])
        resp_sessions = json.loads(response.data.decode("utf-8"))["sessions"]
        for db_actual, resp_actual, expected in zip(db_sessions, resp_sessions, expected_sessions):
            self.assertEqual(resp_actual, expected)
            self.assertEqual(db_actual, expected)
