import itertools, re
from .fourFn import solve

def get_next_session(spec):
    # seed_weight =
    set_gen = get_next_set(spec.pop())
    spec = zip(*[itertools.cycle(x) for x in spec])
    next_session = {}

    while True:
        for sets_in_session, session_weight in spec:
            next_session["sets"] = []
            # curr_weight = calc_weight(curr_weight, session_weight)
            for x in range(sets_in_session):
                next_session["sets"].append(next(set_gen))
            new_spec = yield next_session
            if new_spec:
                set_gen.send(new_spec.pop())
                spec = zip(*[itertools.cycle(x) for x in new_spec])
                break


def get_next_set(spec):
    rep_gen = get_next_rep(spec.pop())
    spec = zip(*[itertools.cycle(x) for x in spec])
    next_set = {}

    while True:
        for set_rest, set_weight, reps_in_set in spec:
            # curr_weight = calc_weight(curr_weight, set_weight)
            next_set["rest"] = set_rest
            next_set["reps"] = []
            for x in range(reps_in_set):
                next_set["reps"].append(next(rep_gen))
            new_spec = yield next_set
            if new_spec:
                rep_gen.send(new_spec.pop())
                spec = zip(*[itertools.cycle(x) for x in new_spec])
                break


def get_next_rep(spec):
    spec = zip(*[itertools.cycle(x) for x in spec])

    while True:
        for rep_time, rep_rest, rep_weight in spec:
            # curr_weight = calc_weight(rep_weight)
            new_spec = yield {"time_on": rep_time, "time_off": rep_rest}#, "weight": curr_weight}
            if new_spec:
                spec = zip(*[itertools.cycle(x) for x in new_spec])
                break

def calc_weight(base, transform):
    transform = re.sub(r'[Xx]', str(base), transform)
    return solve(transform)
