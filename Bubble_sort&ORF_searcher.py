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


def find_ORFs(sequence, reversecomplement=False):
    """
    :param sequence: input sequence, where you want to find your ORFS, from 5' to 3'.
    :param reversecomplement: just something I needed to use recursion. Don't event think about this argument.
    :return: all the ORFs in the sequence and its reverse compement
    """
    sequence = sequence.upper()
    ORFs = []
    for iter in range(3): # we look in al 3 reading frames
        starts, finish = [], None
        seq = sequence[iter:]
        for i in range(0, len(seq), 3):
            codon = seq[i:i+3]
            if codon == "ATG":
                starts.append(i) # open an orf
            if codon in {"TAG", "TAA", "TGA"} and starts: # If there is start and you encounter stop
                finish = i+3
                for start in starts:
                    if i-start >=9: # if there are at least 4 codons
                        # ATG NNN NNN TAA
                        # 0           9
                        # i-start = 9
                        ORFs.append(seq[start:finish])
                starts = [] # Close an orf anyways (even if it's too short)
    # Now I add reverse complement ORFs to it.
    compl = {"A": "T", "T": "A", "C": "G", "G": "C"}
    additions = []
    if not reversecomplement:
        sequence = "".join([compl[letter] for letter in sequence][::-1])
        additions = find_ORFs(sequence, reversecomplement=True)
    return ORFs + additions

sq = "ATG" \
     "ACT" \
     "CCT" \
     "TAA" \
     "TGA" \
     "ATG" \
     "TGG" \
     "ATG" \
     "GTA" \
     "CGT" \
     "GTA" \
     "TAA" \
     "GATCGGTGCTAGCACTGTACAGTGTCATGACTACACGTGTACGTACTAACATGACATGTGATACACACATAAACTATCGCGGGATCTAACTTA"
print(find_ORFs(sq))