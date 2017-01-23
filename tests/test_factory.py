from application.utils import factory
from testing_config import BaseTestConfig

class TestFactory(BaseTestConfig):
    def test_get_next(self):
        weights = {
            "session": ["0.9*X"],
            "set":[["0.65*X", "0.75*X", "0.85*X"],
                ["0.7*X", "0.8*X", "0.9*X"],
                ["0.75*X", "0.85*X", "0.95*X"],
                ["0.4*X", "0.5*X", "0.6*X"]],
            "rep": [["X"]]
        }
        times = {
            "session": [],
            "set":[[180, 150]],
            "rep":[[[10,6,2], [5,3,1]], [[6,2], [3,1]], [[2],[1]]]
        }
        freqs = {
            "session": [2, 2, 2, 1],
            "set":[3],
            "rep":[3,2,2]
        }
        gen = factory.get_next(111.111111111111111111111111111111111, weights, times, freqs)

        expected_sessions = [{
            'sets': [{
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 65.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 65.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 65.0
                }], 'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 75.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 85.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 65.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 65.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 65.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 75.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 85.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 70.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 70.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 80.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 80.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 90.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 90.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 70.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 70.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 80.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 80.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 90.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 90.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 95.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 95.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 95.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 95.0
                }], 'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 40.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 40.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 40.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 50.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 50.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 50.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 10, 'ordinal': 0, 'time_off': 5, 'weight': 60.0
                }, {
                    'time_on': 6, 'ordinal': 1, 'time_off': 3, 'weight': 60.0
                }, {
                    'time_on': 2, 'ordinal': 2, 'time_off': 1, 'weight': 60.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 65.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 65.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 65.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 65.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 75.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 75.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 6, 'ordinal': 0, 'time_off': 3, 'weight': 85.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 85.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }, {
            'sets': [{
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 70.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 70.0
                }],
                'rest': 180, 'ordinal': 0
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 80.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 80.0
                }],
                'rest': 150, 'ordinal': 1
            }, {
                'reps': [{
                    'time_on': 2, 'ordinal': 0, 'time_off': 1, 'weight': 90.0
                }, {
                    'time_on': 2, 'ordinal': 1, 'time_off': 1, 'weight': 90.0
                }],
                'rest': 180, 'ordinal': 2
            }]
        }]

        for expected in expected_sessions:
            self.assertEqual(next(gen), expected)


    def test_calc_weight(self):
        curr_weight = 180
        weights = ["X+1", "X-10", "X*0.75", "X/3", "x+(X*0.04)"]
        expected_weights = [181, 171, 128.25, 42.75, 44.46]

        for weight, expected in zip(weights, expected_weights):
            curr_weight = factory.calc_weight(curr_weight, weight)
            self.assertEqual(curr_weight, expected)
