from Bio.pairwise2 import format_alignment
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.Alphabet import generic_rna

def align_sequence(seq, dot):
    # seq = "GCUUACGGCCAUACCACCUUAGGCGUGCCCGAUCUCGUCUGAUCUCGGAAGCUAAGCAGGGUCGGGCCUGGUUAGUA"
    # dot = "....((((((....))))))((....((((((.............))........))))))................"
    min_pairs = 3  # Should be paramether TODO: account for - different scenarious of usability
    result = ["." for _ in range(len(dot))]
    edges = [] # Contains pairs of left and right indices


    def process_stem(ix):
        c = dot[ix]
        stack = []
        while c != ")" and ix != len(dot):  # Search for group of brackets
            if c == "(":
                stack.append(ix)
            ix += 1
            if ix == len(dot):
                print("Brackets don't match!")
                exit(0)
            c = dot[ix]
        fst = None
        if len(stack) == 0 or ix == len(dot):
            return -1
        while c != "(" and ix != len(dot):  # End of group
            if c == ")":
                fst = stack.pop()  # Ищем первый индекс
            ix += 1
            if ix == len(dot):
                if len(stack) == 0:
                    break
                else:
                    print("Brackets don't match!")
                    exit(0)
            c = dot[ix]
        snd = ix
        perc = 0.3
        # perc = 5
        width = snd - fst
        # Equal step in both directions
        fst = 0 if fst - perc * width / 2 < 0 else int(fst - (perc * width) / 2)
        snd = len(dot) if snd + perc * width / \
            2 > len(dot) else int(snd + (perc * width) / 2)
        # print(fst, snd, dot[fst:snd])
        middle = (snd - fst) // 2 + fst  # Maybe more elaboration on this one
        # print(fst, middle, snd)

        for l_edge,r_edge in edges: # Fix intervals if they intersect
            if fst<r_edge:
                fst=r_edge+1
        left = seq[fst:middle + 1]
        right = seq[middle + 1:snd]
        if len(left) == 0:
            return ix
        # print(len(left), len(right), left, right)
        # We will search for stem here
        my_rna = Seq(right, generic_rna)
        # We align complement here, so we will need to return to original sequence
        right = my_rna.reverse_complement()
        # print(left, right)
        al = pairwise2.align.localms(left, right, 100, -150, -100,
                                     -100, one_alignment_only = True)  # Match, mismatch, open, extend
        # TODO: Choose best variant. Now we take the first one
        al_left_full, al_right_full, _, start, end = al[0]
        # print(format_alignment(*al[0]))
        # print(al_left_full, al_right_full)
        al_left = al_left_full[start:end]
        al_right = al_right_full[start:end]
        # Now we need a metric of alignament quality. To start with, we will use basic number of matches metric
        matches_threshold = 0.5
        matches = 0
        for i in range(len(al_left)):
            if al_left[i] == al_right[i]:
                matches += 1
        matches_rate = matches / len(al_left)
        if matches_rate > matches_threshold and matches >= min_pairs:
            ptr = fst
            for i in range(start):
                if al_left_full[i] != "-":
                    ptr += 1
            # print(seq[ptr:middle+1])
            gaps = 0  # We count gaps not to skip it in original sequence
            # print(al_right, seq[i:])
            left_edge = None
            right_edge = None
            for i in range(len(al_left)):
                if al_left[i] == "-":
                    gaps += 1
                if al_left[i] == al_right[i]:
                    if left_edge is None:
                        left_edge = ptr + i - gaps
                    result[ptr + i - gaps] = "("
                    # print(al_left[i])
            ptr = snd
            for i in range(start):
                if al_right_full[i] != "-":
                    ptr -= 1  # We go from the end, because we have reversed alignment
            # print(seq[middle+1:ptr])
            gaps = 0
            for i in range(len(al_left)):
                if al_right[i] == "-":
                    gaps += 1
                if al_left[i] == al_right[i]:
                    if right_edge is None or ptr - i - 1 + gaps > right_edge:
                        right_edge = ptr - i - 1 + gaps
                    result[ptr - i - 1 + gaps] = ")"
            if left_edge is not None and right_edge is not None:
                edges.append((left_edge, right_edge))
            # print(edges)

        return ix


    ret = 0
    while ret != len(dot):
        ret = process_stem(ret)
    #     print(ret, dot[ret:])
    # print(seq)
    # print(''.join(result))
    return ''.join(result)

if __name__ == '__main__':
    import sys
    print(align_sequence(sys.argv[1], sys.argv[2]))
