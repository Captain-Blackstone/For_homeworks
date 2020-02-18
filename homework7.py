"""Hello, Sasha!
I guess, I give up making funny homeworks from now on. How can I make funny an alignment algorithm? Align two
names of creatures? Hm. Not that bad. Anyway, a can't come up with a good pair of creatures names..."""

from Bio import SeqIO
from homework4 import flatten
import numpy as np

class color:
   GREEN = '\033[92m'
   END = '\033[0m'

def fastq2fasta(input_file, output_file, min_length=50):
    """
    This one converts your fastq file to fast, removing short sequences
    :param fastq: path to your fastq file
    :param fasta: path where you want to place the resulting fasta file
    :param min_length: length, below which sequences will be dropped
    :return: None
    """
    fastq = SeqIO.parse(input_file, "fastq")
    fastq = [record for record in fastq if len(record.seq) >= min_length]
    SeqIO.write(fastq, output_file, "fasta")


def match_mismatch(score, penalty, i, j, seq1, seq2):
    """
    This little one gets me an appropriate score for placing letters opposite each other depending on weather they
    are the same or not
    :param score: match score. Probably 0 or negative
    :param penalty: musmatch penalty
    :param i: position in seq1
    :param j: position in seq2
    :param seq1: first sequence
    :param seq2: second sequence
    :return: score or penalty dependent on match or mismatch
    """
    return score if seq1[i] == seq2[j] else penalty


def Needleman_Wunsch(file, match=0, mismatch=1, gap=1):
    """
    Function performs a global alignment of two sequences
    :param file: fasta file with two sequences you want to align
    :param match: match score
    :param mismatch: mismatch penalty
    :param gap: gap penalty. Yes, I just added the word "score" or "penalty" and considered this explanation to be clear.
    :return: a tuple of two elements: the total score of alignment and two aligned lines
    """
    seqs = list(SeqIO.parse(file, "fasta"))
    first = str(seqs[0].seq)
    second = str(seqs[1].seq) # Now we have two sequences we want to align
    len1 = len(first)
    len2 = len(second)
    score_matrix = np.array([np.zeros(len1+1) for _ in range(len2+1)]) # initiates a score matrix filled with zeros
    # Now let's fill the first column and the first row
    score = 0
    for i in range(len1+1):
        score_matrix[0][i] += score
        score += gap
    score = 0
    for j in range(len2+1):
        score_matrix[j][0] += score
        score += gap
    # Next let's fill all the matrix, going row by row
    for j in range(1, len2+1):
        for i in range(1, len1+1):
            score1 = score_matrix[j][i-1] + gap
            score2 = score_matrix[j-1][i] + gap
            score3 = score_matrix[j-1][i-1] + match_mismatch(match, mismatch, i-1, j-1, first, second)
            # i-1 and j-1 in the match_mismatch arise because in the matrix the i-th position doesn't correspond to
            # the i-th position in the sequence - because position i=0, j=0 is a position of gap-gap. So every
            # position in sequence is a position in matrix - 1. These inconvenient i-1 and j-1 will arise further
            # when I'll interact with sequences more.
            score = min(score1, score2, score3)
            score_matrix[j][i] += score
    # Backtracking
    i = len(first)
    j = len(second)
    alignment = ["", ""]
    while not (i==0 and j ==0): # While haven't reached the upper left corner
        diagonal = score_matrix[j-1][i-1] + match_mismatch(match, mismatch, i-1, j-1, first, second)
        left = score_matrix[j][i-1] + gap
        up = score_matrix[j-1][i] + gap
        if i == 0: # if reached left side, we just go straight up. Not very elegant.
            next_one = up
            diagonal = next_one + 1
            left = next_one + 1
        elif j == 0: # if reached upper side, just go straight left.
            next_one = left
            diagonal = next_one + 1
            up = next_one + 1
        else:
            next_one = min(diagonal, left, up) # if inside the matrix, choose a path according to the scores
        # Add a little piece to alignment. Notice, that initially it is a backward alignment, but I'll reverse it
        # at the end
        if diagonal == next_one:
            alignment[0] += first[i-1] # I promised more of this i-1, j-1 stuff.
            alignment[1] += second[j-1]
            i -= 1
            j -= 1
        elif left == next_one:
            alignment[0] += first[i-1]
            alignment[1] += "-"
            i -= 1
        elif up == next_one:
            alignment[0] += "-"
            alignment[1] += second[j-1]
            j -= 1
    return -score_matrix[len2][len1], alignment[0][::-1] + "\n" + alignment[1][::-1]


def Smith_Waterman(file, match=1, mismatch=-1, gap=-1):
    """
    performs local alignment
    :param file: a fasta file with two sequences, the first one is the one we search in, and the second one is a query
    :param match: match score, positive
    :param mismatch: mismatch penalty, negative
    :param gap: gap penalty, negative
    :return: a tuple of two values, alignment score and an alignment itself
    """
    seqs = list(SeqIO.parse(file, "fasta"))
    first = str(seqs[0].seq)
    second = str(seqs[1].seq)  # Now we have two sequences we want to align
    len1 = len(first)
    len2 = len(second)
    score_matrix = np.array([np.zeros(len1 + 1) for _ in range(len2 + 1)])  # initiates a score matrix filled with zeros
    # Next let's fill all the matrix, going row by row
    for j in range(1, len2 + 1):
        for i in range(1, len1 + 1):
            score1 = score_matrix[j][i - 1] + gap
            score2 = score_matrix[j - 1][i] + gap
            score3 = score_matrix[j - 1][i - 1] + match_mismatch(match, mismatch, i - 1, j - 1, first, second)
            # i-1 and j-1 in the match_mismatch arise because in the matrix the i-th position doesn't correspond to
            # the i-th position in the sequence - because position i=0, j=0 is a position of gap-gap. So every
            # position in sequence is a position in matrix - 1. These inconvenient i-1 and j-1 will arise further
            # when I'll interact with sequences more.
            score = max(score1, score2, score3, 0)
            score_matrix[j][i] += score
    # Now let's find the maximum value. Not sure the way I do it is the most efficient...
    numbers = flatten(list([list(raw) for raw in score_matrix]))
    for k in range(len2+1):
        for l in range(len1+1):
            if score_matrix[k][l] == max(numbers):
                i = l
                j = k
                break
    # This is a tough one. Here I start an alignment with two pieces, which were not aligned.
    # first[i:][::-1] - this is reverted end of reference, after an alignment
    # second[j:] - this is unaligned end of query
    # "-"*(len(first[i:])-len(second[j:])) - this is "-" repeated as many times, as the length of unaligned
    # reference minus length of unaligned end of query
    alignment = [first[i:][::-1], str(second[j:]+"-"*(len(first[i:])-len(second[j:])))[::-1]]
    while score_matrix[j][i] != 0:
        diagonal = score_matrix[j - 1][i - 1]
        left = score_matrix[j][i - 1]
        up = score_matrix[j - 1][i]
        next_one = max(diagonal, left, up)
        if diagonal == next_one:
            alignment[0] += first[i-1]
            alignment[1] += color.END[::-1] + second[j-1] + color.GREEN[::-1] # A little magic. I want the aligned
            # part to be highlighted in green, but as I will reverse this sequence in future, I need to write reverses
            # of color keywords...
            i -= 1
            j -= 1
        elif left == next_one:
            alignment[0] += first[i-1]
            alignment[1] += color.END[::-1] + "-" + color.GREEN[::-1]
            i-=1
        elif up == next_one:
            alignment[0] += "-"
            alignment[1] += color.END[::-1] + second[j-1] + color.GREEN[::-1]
            j -= 1
    alignment[0] = alignment[0][::-1] # reverse the sequences
    alignment[1] = alignment[1][::-1]
    alignment[0] = first[:i] + alignment[0] # add unaligned start of reference.
    alignment[1] = "-"*(len(first[:i])-len(second[:j])) + second[:j] + alignment[1]
    # add unaligned start of query. The construction is similar to one at the start of a loop - where I added
    # the unaligned end
    return max(numbers), "\n".join(alignment)



# fastq2fasta("sample.fastq", "sample.fasta")
# alignment = Needleman_Wunsch("sample.fasta")
# print(alignment[0])
# print(alignment[1])
# alignment = Smith_Waterman("sample.fasta")
# print(alignment[0])
# print(alignment[1])
alignment = Smith_Waterman("gag.fasta")
print(alignment[0])
print(alignment[1])