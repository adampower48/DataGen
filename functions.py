import string

import numpy as np


def gen_strings(n, l, chars=string.ascii_letters):
    idxs = np.random.randint(len(chars), size=(n, l))
    return ["".join(map(chars.__getitem__, idxs[i])) for i in range(n)]


def gen_ints(n, low, high):
    return np.random.randint(low, high, n)


def gen_floats(n, low, high, precision=None):
    l = np.random.rand(n) * (high - low) + low

    if precision:
        lam = lambda x: round(x, precision)
        return list(map(lam, l))

    return l


def from_list(n, li, p=None):
    return np.random.choice(li, size=n, p=p)


def gen_set(n, *data):
    # data: (type, *params)
    func_maps = {
        int: gen_ints,
        float: gen_floats,
        str: gen_strings,
        list: from_list,
    }

    for d in data:
        try:
            func_maps[d[0]](1, *d[1:])
        except TypeError:
            print("Incorrect format", d)
            return []

    out = []
    for d in data:
        out.append(func_maps[d[0]](n, *d[1:]))

    return list(zip(*out))


if __name__ == '__main__':
    print(gen_strings(10, 5))
    print(gen_ints(10, 1, 7))
    print(gen_floats(10, 1, 7))
    print(from_list(10, ["Hello", "There", "General", "Kenobi"]))

    print(*gen_set(10, (str, 10), (int, 10, 20), (list, ["Brown", "Black", "Blonde", "Ginger"]), (float, 150, 200, 2)),
          sep="\n")
