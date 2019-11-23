# Hello, Sasha!
# I hope your depression has come to an end. You're a really good and motivated teacher! Don't take too seriously
# your problems with administration.

def bubble_sort(lst):
    for i in range(len(lst)):
        print(lst)
        already_sorted = True
        for j in range(len(lst)-1):
            if lst[j] > lst[j+1]:
                already_sorted = False
                lst[j], lst[j+1] = lst[j+1], lst[j]
        if already_sorted:
            break
    return lst

x = [5, 3, 2, 5, 6, 1, 6, 7, 4, 3, 9, 10, 4]
bubble_sort(x)


def find_ORFs(sequence):
    ORFs = []
    for iter in range(3): # we look in al 3 reading frames
        start, finish = None, None
        seq = sequence[iter:]
        for i in range(0, len(seq), 3):
            codon = seq[i:i+3]
            if codon == "ATG":
                start = i # open an orf
            if codon in {"TAG", "TAA", "TGA"} and not start is None: # If there is start and you encounter stop
                finish = i+3
                if i-start >=9: # if there are at least 4 codons
                    # ATG NNN NNN TAA
                    # 0           9
                    # i-start = 9
                    ORFs.append(seq[start:finish])
                start = None # Close an orf anyways (even if it's too short)
    return ORFs

sq = "ATG" \
     "ACT" \
     "CCT" \
     "TAATGAAGCTAGTACGTACGTGTACACGATCGGTGCTAGCACTGTACAGTGTCATGACTACACGTGTACGTACTAACATGACATGTGATACACACATAAACTATCGCGGGATCTAACTTA"
print(find_ORFs(sq))