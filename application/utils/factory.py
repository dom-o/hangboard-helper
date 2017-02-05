import itertools, re
from .fourFn import solve

def get_next(base, weights, times, freqs):
    curr_weight = calc_weight(base, weights["pre"])
    for sesh_weight, sesh_freq, set_weights, set_times, set_freqs, rep_weights, rep_times, rep_freq in zip(itertools.cycle(weights["session"]), itertools.cycle(freqs["session"]), itertools.cycle(weights["set"]), itertools.cycle(times["set"]), itertools.cycle(freqs["set"]), itertools.cycle(weights["rep"]), itertools.cycle(times["rep"]), itertools.cycle(freqs["rep"])):
        next_session = {"sets":[]}
        curr_weight = calc_weight(curr_weight, sesh_weight)
        set_incr = 0
        for x, set_weight, set_rest in zip(range(set_freqs), itertools.cycle(set_weights), itertools.cycle(set_times)):
            next_set = {"reps":[], "rest":-1}
            rep_incr = 0
            curr_set_weight = calc_weight(curr_weight, set_weight)
            for x, on, off, weight in zip(range(rep_freq), itertools.cycle(rep_times[0]), itertools.cycle(rep_times[1]), itertools.cycle(rep_weights)):
                curr_rep_weight = calc_weight(curr_set_weight, weight)
                next_rep = {"time_on":on, "time_off":off, "weight": curr_rep_weight, "ordinal": rep_incr}
                rep_incr += 1
                next_set["reps"].append(next_rep)
            next_set["rest"] = set_rest
            next_set["ordinal"] = set_incr
            set_incr += 1
            next_session["sets"].append(next_set)
        for x in range(sesh_freq):
            yield next_session


def calc_weight(base, transform):
    transform = re.sub(r'[xX]', str(base), transform)
    return solve(transform)
