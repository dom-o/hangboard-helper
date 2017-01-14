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
