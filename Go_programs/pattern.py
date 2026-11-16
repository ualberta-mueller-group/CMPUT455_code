# Cmput 455 sample code
# 33 Patterns
# Written by Chenjun Xiao
# Code is from the michi project on Github:
# https://github.com/pasky/michi/blob/master/michi.py

from functools import reduce
from typing import List, Set

# 3x3 playout patterns
# X,O are colors
# x,o are the "inverses" of X,O: the other color, or empty

Pattern = List[str]

pat3src: List[Pattern] = [  
    ["XOX", "...", "???"],  # hane pattern - enclosing hane
    ["XO.", "...", "?.?"],  # hane pattern - non-cutting hane
    ["XO?", "X..", "x.?"],  # hane pattern - magari
    # ["XOO",  # hane pattern - thin hane
    #  "...",
    #  "?.?", "X",  - only for the X player
    [
        ".O.",  # generic pattern - katatsuke or diagonal attachment; similar to magari
        "X..",
        "...",
    ],
    ["XO?", "O.o", "?o?"],  # cut1 pattern (kiri] - unprotected cut
    ["XO?", "O.X", "???"],  # cut1 pattern (kiri] - peeped cut
    ["?X?", "O.O", "ooo"],  # cut2 pattern (de]
    ["OX?", "o.O", "???"],  # cut keima
    ["X.?", "O.?", "   "],  # side pattern - chase
    ["OX?", "X.O", "   "],  # side pattern - block side cut
    ["?X?", "x.O", "   "],  # side pattern - block side connection
    ["?XO", "x.x", "   "],  # side pattern - sagari
    ["?OX", "X.O", "   "],  # side pattern - cut
]


def pat3_expand(pat: Pattern) -> Pattern:
    """ All possible neighborhood configurations matching a given pattern;
        used just for a combinatoric explosion when loading them in an
        in-memory set. """

    def pat_rot90(p: Pattern) -> Pattern:
        return [
            p[2][0] + p[1][0] + p[0][0],
            p[2][1] + p[1][1] + p[0][1],
            p[2][2] + p[1][2] + p[0][2],
        ]

    def pat_vertflip(p: Pattern) -> Pattern:
        return [p[2], p[1], p[0]]

    def pat_horizflip(p: Pattern) -> Pattern:
        return [l[::-1] for l in p]

    def pat_swapcolors(p: Pattern) -> Pattern:
        return [
            l.replace("X", "Z")
            .replace("x", "z")
            .replace("O", "X")
            .replace("o", "x")
            .replace("Z", "O")
            .replace("z", "o")
            for l in p
        ]

    def pat_wildexp(p: str, c: str, to: List[str]) -> Pattern:
        i = p.find(c)
        if i == -1:
            return [p]
        return reduce(
            lambda a, b: a + b, [pat_wildexp(p[:i] + t + p[i + 1 :], c, to) for t in to]
        )

    def pat_wildcards(pat: str) -> Pattern:
        return [
            p3
            for p in pat_wildexp(pat, "?", list(".XO "))
            for p2 in pat_wildexp(p, "x", list(".O "))
            for p3 in pat_wildexp(p2, "o", list(".X "))
        ]

    return [
        p
        for p1 in [pat, pat_rot90(pat)]
        for p2 in [p1, pat_vertflip(p1)]
        for p3 in [p2, pat_horizflip(p2)]
        for p4 in [p3, pat_swapcolors(p3)]
        for p in pat_wildcards("".join(p4))
    ]

pat3list: Pattern = [p.replace("O", "x") for pl in pat3src for p in pat3_expand(pl)]
pat3set: Set[str] = set(pat3list)
