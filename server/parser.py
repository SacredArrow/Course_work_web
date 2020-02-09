from PIL import Image
import numpy as np
import sys
import os
from lark import Lark
# s = "GCUUACGGCCAUACCACCUUAGGCGUGCCCGAUCUCGUCUGAUCUCGGAAGCUAAGCAGGGUCGGGCCUGGUUAGUA"
s = "CCCCCUCUCAAAUCCUUGGAACCUAGGUGUGAGUGCUGCUCUAGUGCAACACACCUAUUCAAGGAUUCAAAGAGGCUGA"
# grammar = """
# start:stem
# any_str:ANY~1..20
# s0: any_str | any_str stem s0
# ANY: "A" | "U" | "G" | "C"
# PAIRA: "A"
# PAIRC: "C"
# PAIRG: "G"
# PAIRU: "U"
# pairg: PAIRG
# pairc: PAIRC
#
# stem1: PAIRA s0 PAIRU |
#         pairg s0 pairc |
#         PAIRC s0 PAIRG |
#         PAIRU s0 PAIRA
# stem2: PAIRA stem1 PAIRU |
#         PAIRG stem1 PAIRC |
#         PAIRC stem1 PAIRG |
#         PAIRU stem1 PAIRA
# stem: PAIRA stem PAIRU |
#         PAIRG stem PAIRC |
#         PAIRC stem PAIRG |
#         PAIRU stem PAIRA |
#         PAIRA stem2 PAIRU |
#                 PAIRG stem2 PAIRC |
#                 PAIRC stem2 PAIRG |
#                 PAIRU stem2 PAIRA
# %import common.WS
# %ignore WS
# """
# l = Lark(grammar)
# print(l.parse(s))
def fits (a,b):
    if (a == "C" and b == "G") or (a == "G" and b == "C") or (a == "A" and b == "U") or (a == "U" and b == "A"):
        return True
    else:
        return False

size = len(s)
mtrx = []
min_stem_len = 3
bases_in_a_row = 3
for i in range(len(s)-2*bases_in_a_row-min_stem_len): # Doubtable formulas
    for j in range(i+bases_in_a_row+min_stem_len, len(s)-bases_in_a_row):
        # if ((s[i] == "C" and s[j] == "G") or \
        # (s[i] == "G" and s[j] == "C") or \
        # (s[i] == "U" and s[j] == "A") or \
        # (s[i] == "A" and s[j] == "U")) and \
        # abs(i-j)>=3:
        #     mtrx.append((i,j))

        for gap in range(min_stem_len,5):
            if j+gap+(bases_in_a_row) >= len(s):
                continue
            bool = True
            for k in range(bases_in_a_row):
                if fits(s[i+k], s[j+gap+(bases_in_a_row - k)]):
                    continue
                else:
                    bool = False
            if bool:
                mtrx.append((j,i))
# print(mtrx)
img = Image.new('L', (size, size), (0)) # Black background, white points
pixels = np.array(img)
for el in mtrx:
    x, y = el
    pixels[x][y] = 255
    #pixels[y][x] = 255 #for mirrored squares
Image.fromarray(pixels).save('out.png')
