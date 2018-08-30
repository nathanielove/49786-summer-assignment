from solution.models import Segment


def remove_sub_segments(segments):
    Segment.sort_by_start(segments)

    result = []
    i = 0

    while i < len(segments):
        result.append(segments[i])

        j = i + 1
        while j < len(segments) and segments[i].covers(segments[j]):
            j += 1

        i = j

    return result


def add(first, second, coverage):
    if second.overlaps(first):
        coverage += second.size() - second.intersection(first).size()
    else:
        coverage += second.size()

    return coverage


def brute_force_merge(segments):
    s = segments[0].size()
    for i in range(1, len(segments)):
        s = add(segments[i - 1], segments[i], s)
    return s


def solve_by_brute_force(segments):
    segments = remove_sub_segments(segments)
    m = 0

    checkpoints = set([int(x / 100 * len(segments)) for x in range(1, 101)])

    for i in range(len(segments)):
        m = max(m, brute_force_merge(segments[:i] + segments[i + 1:]))
        if i in checkpoints:
            print('Completed: {p}%'.format(p=int(i * 100 / len(segments))))

    return m


def generate_increments(segments):
    coverages = [segments[0].size(), add(segments[0], segments[1], segments[0].size())]
    for i in range(2, len(segments)):
        coverage = add(segments[i - 1], segments[i], coverages[-1])
        coverages.append(coverage)
    return coverages


def solve_by_dp(segments):
    reduced = remove_sub_segments(segments)

    if len(reduced) < 2:
        return 0 if len(segments) < 2 else reduced[0].size()

    if len(reduced) == 2:
        return max(reduced, key=lambda x: x.size()).size()

    forward = generate_increments(reduced)
    backward = generate_increments(list(reversed(reduced)))
    backward.reverse()

    m = max(forward[-2], backward[1])

    for i in range(1, len(reduced) - 1):
        m = max(m, forward[i - 1] + backward[i + 1])

    return m
