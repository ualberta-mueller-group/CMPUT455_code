# Cmput 455 sample code
# 33 Pattern learning
# Written by Chenjun Xiao
# Code is from the michi project on Github:
# https://github.com/pasky/michi/blob/master/michi.py

import collections
from functools import reduce
from pattern import pat3list, Pattern
from typing import Dict

def switch_color(pattern: str) -> str:
    p = pattern
    p = p.replace("x", "O")
    p = p.replace("X", "x")
    p = p.replace("O", "X")
    return p

def generate_pattern_index(pat3list: Pattern) -> Dict[str, int]:
    """
    Assign all symmetric patterns to the same pattern index, 
    which is used for learning.
    There are three types of symmetry: 
        rotation symmetry
        reflection symmetry
        color symmetry.
    """
    index = 0
    p_index = {}
    for p in pat3list:
        if p in p_index:
            continue
        p1 = p[6] + p[3] + p[0] + p[7] + p[4] + p[1] + p[8] + p[5] + p[2]
        p2 = p[8] + p[7] + p[6] + p[5] + p[4] + p[3] + p[2] + p[1] + p[0]
        p3 = p[2] + p[5] + p[8] + p[1] + p[4] + p[7] + p[0] + p[3] + p[6]
        p4 = p[6] + p[7] + p[8] + p[3] + p[4] + p[5] + p[0] + p[1] + p[2]
        p5 = p[2] + p[1] + p[0] + p[5] + p[4] + p[3] + p[8] + p[7] + p[6]
        p6 = p[0] + p[3] + p[6] + p[1] + p[4] + p[7] + p[2] + p[5] + p[8]
        p7 = p[8] + p[5] + p[2] + p[7] + p[4] + p[1] + p[6] + p[3] + p[0]
        p_index[p] = index
        p_index[p1] = index
        p_index[p2] = index
        p_index[p3] = index
        p_index[p4] = index
        p_index[p5] = index
        p_index[p6] = index
        p_index[p7] = index

        p_index[switch_color(p)] = index
        p_index[switch_color(p1)] = index
        p_index[switch_color(p2)] = index
        p_index[switch_color(p3)] = index
        p_index[switch_color(p4)] = index
        p_index[switch_color(p5)] = index
        p_index[switch_color(p6)] = index
        p_index[switch_color(p7)] = index
        index += 1
    return p_index

patIndex: Dict[str, int] = generate_pattern_index(pat3list)
