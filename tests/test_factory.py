from application.utils import factory
from testing_config import BaseTestConfig

class TestFactory(BaseTestConfig):
    def test_get_next_rep(self):
        times = [12, 6, 4, 2]
        rests = [12]
        weights = ["X+0"]

        rep_generator = factory.get_next_rep([times, rests, weights])
        next_rep = next(rep_generator)
        self.assertEqual(next_rep, {"time_on": 12, "time_off": 12})
        next_rep = next(rep_generator)
        self.assertEqual(next_rep, {"time_on": 6, "time_off": 12})

        new_times = [2, 4, 8]
        new_rests = [1, 2, 4]
        new_weights = ["X"]
        next_rep = rep_generator.send([new_times, new_rests, new_weights])
        self.assertEqual(next_rep, {"time_on": 2, "time_off": 1})
        next_rep = next(rep_generator)
        self.assertEqual(next_rep, {"time_on": 4, "time_off": 2})

    def test_get_next_set(self):
        rests = [180]
        weights = ["X", "X+10", "X+20"]
        num_reps = [7, 6, 5]
        rep_spec = [[7],[3],["X"]]

        set_generator = factory.get_next_set([rests, weights, num_reps, rep_spec])

        next_set = next(set_generator)
        self.assertEqual(next_set["rest"], 180)
        self.assertEqual(len(next_set["reps"]), 7)
        self.assertEqual(next_set["reps"][0], {"time_on": 7, "time_off": 3})

        next_set = next(set_generator)
        self.assertEqual(next_set["rest"], 180)
        self.assertEqual(len(next_set["reps"]), 6)
        self.assertEqual(next_set["reps"][0], {"time_on": 7, "time_off": 3})

        new_rests = [120, 90]
        new_weights = ["X"]
        new_num_reps = [7, 2]
        new_rep_spec = [[5],[5],["X"]]

        next_set = set_generator.send([new_rests, new_weights, new_num_reps, new_rep_spec])
        self.assertEqual(next_set["rest"], 120)
        self.assertEqual(len(next_set["reps"]), 7)
        self.assertEqual(next_set["reps"][0], {"time_on": 5, "time_off": 5})

        next_rep = next(set_generator)
        self.assertEqual(next_set["rest"], 90)
        self.assertEqual(len(next_set["reps"]), 2)
        self.assertEqual(next_set["reps"][0], {"time_on": 5, "time_off": 5})

    def test_get_next_session(self):
        sets_in_session = [3, 6, 7]
        session_weight = ["X"]
        set_spec = [ [180], ["X", "X+10", "X+20"], [7, 6, 5], [[7],[3],["X"]] ]
        session_generator = factory.get_next_session([sets_in_session, session_weight, set_spec])

        next_session = next(session_generator)
        self.assertEqual(len(next_session["sets"]), 3)
        next_session = next(session_generator)
        self.assertEqual(len(next_session["sets"]), 6)

        new_sets_in_session = [2]
        new_session_weight = ["X"]
        new_set_spec = [ [120, 90], ["X"], [7, 2], [[5],[5],["X"]] ]
        next_session = session_generator.send([new_sets_in_session, new_session_weight, new_set_spec])
        self.assertEqual(len(next_session["sets"]), 2)
        next_session = next(session_generator)
        self.assertEqual(len(next_session["sets"]), 2)

    def test_calc_weight(self):
        curr_weight = 180
        weights = ["X+1", "X-10", "X*0.75", "X/3", "x+(X*0.04)"]
        expected_weights = [181, 171, 128.25, 42.75, 44.46]

        for weight, expected in zip(weights, expected_weights):
            curr_weight = factory.calc_weight(curr_weight, weight)
            self.assertEqual(curr_weight, expected)
