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
        "str_custom": gen_strings_format,
    }

    for d in data:
        # Check valid formats
        try:
            func_maps[d[0]](1, *d[1:])
        except TypeError:
            print("Incorrect format", d)
            return []

    out = []
    # Generate data
    for d in data:
        out.append(func_maps[d[0]](n, *d[1:]))

    return list(zip(*out))


def gen_strings_format(n, *formats):
    # i: integer 0-9
    # c: char a-z
    # C: char A-Z
    # s: char a-z + A-Z
    # l: lXXXXXXXXXX choice from list of chars. eg labc123
    # w: wdXXXXXXXXX choice from list of strings, separated by delimiter d. eg w,my,name,is,joe
    valid = "icCslw"

    func_maps = {
        "i": lambda: gen_ints(n, 0, 10),
        "c": lambda: gen_strings(n, 1, chars=string.ascii_lowercase),
        "C": lambda: gen_strings(n, 1, chars=string.ascii_uppercase),
        "s": lambda: gen_strings(n, 1, chars=string.ascii_letters),
        "l": lambda ls: from_list(n, ls),
        "w": lambda ls: from_list(n, ls),
    }

    for f in formats:
        if f[0] in valid:
            continue

        raise TypeError("Invalid format specifier:", f)

    out = []
    for f in formats:
        func_args = []

        if f[0] == "l":
            # Lists
            chars = list(f[1:])
            func_args.append(chars)
            f = f[0]

        if f[0] == "w":
            # Strings
            delim = f[1]
            words = f[2:].split(delim)
            func_args.append(words)
            f = f[0]

        out.append(func_maps[f](*func_args))

    # Join strings
    return ["".join(map(str, chars)) for chars in zip(*out)]


if __name__ == '__main__':
    print(gen_strings(10, 5))
    print(gen_ints(10, 1, 7))
    print(gen_floats(10, 1, 7))
    print(from_list(10, ["Hello", "There", "General", "Kenobi"]))

    print(*gen_set(3, (str, 10), (int, 10, 20), (list, ["Brown", "Black", "Blonde", "Ginger"]), (float, 150, 200, 2),
                   ("str_custom", *["w,KR,AD,UR,TS,ML,WM,SS,TD,SB,FH", "l-", "l01", "i"])), sep="\n")
    print(gen_strings_format(10, *["C", "C", "C", "i", "i", "labc123", "w,hello,there,general,kenobi"]))
    print(gen_strings_format(20, *["w,KR,AD,UR,TS,ML,WM,SS,TD,SB,FH", "l-", "l01", "i"]))
