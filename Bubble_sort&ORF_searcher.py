def bubble_sort(lst):
    for i in range(len(lst)):
        print(lst)
        already_sorted = True
        for j in range(len(lst)-1):
            if lst[j] > lst[j+1]:
                already_sorted = False
                lst[j], lst[j+1] = lst[j+1], lst[j]
        if already_sorted:
            print("breaking")
            break
    return lst

x = [5, 3, 2, 5, 6, 1, 6, 7, 4, 3, 9, 10, 4]
bubble_sort(x)


def find_ORFs(sequence):
    ORFs = []
    for _ in range(3):
        start, finish = None, None
        seq = sequence[_:]
        for i in range(0, len(seq), 3):
            codon = seq[i:i+3]
            if codon == "ATG":
                start = i
            if not (start is None) and codon in {"TAG", "TAA", "TGA"}:
                finish = i
                break
        if not(start is None) and finish:
            ORFs.append((start, finish))
    return ORFs

sq = "ATGACTTAACCTAGCTAGTACGTACGTGTACACGATCGGTGCTAGCACTGTACAGTGTCATGACTACACGTGTACGTACACACATGTACACACATAAACTATCGCGGGATCTAACTTA"
print(find_ORF(sq))