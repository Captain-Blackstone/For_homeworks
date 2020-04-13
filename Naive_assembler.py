from homework4 import flatten
import numpy as np
import re
from Bio import SeqIO

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


def local_align(first, second, match=1, mismatch=-1, gap_open=-5, gap_extend=-1):
    """
    performs local alignment
    :param file: a fasta file with two sequences, the first one is the one we search in, and the second one is a query
    :param match: match score, positive
    :param mismatch: mismatch penalty, negative
    :param gap: gap penalty, negative
    :return: a tuple of two values, alignment score and an alignment itself
    """
    len1 = len(first)
    len2 = len(second)
    score_matrix = np.array([np.zeros(len1 + 1) for _ in range(len2 + 1)])  # initiates a score matrix filled with zeros
    path_matrix = [["000" for i in range(len1 + 1)] for _ in range(len2 + 1)]
    # Next let's fill all the matrix, going row by row
    gap_open_or_extend = lambda condition: gap_open if not condition else gap_extend
    opened = False
    for j in range(1, len2 + 1):
        for i in range(1, len1 + 1):
            score1 = score_matrix[j][i - 1] + gap_open_or_extend(opened)
            score2 = score_matrix[j - 1][i] + gap_open_or_extend(opened)
            score3 = score_matrix[j - 1][i - 1] + match_mismatch(match, mismatch, i - 1, j - 1, first, second)
            # i-1 and j-1 in the match_mismatch arise because in the matrix the i-th position doesn't correspond to
            # the i-th position in the sequence - because position i=0, j=0 is a position of gap-gap. So every
            # position in sequence is a position in matrix - 1. These inconvenient i-1 and j-1 will arise further
            # when I'll interact with sequences more.
            score = max(score1, score2, score3, 0)
            path = [1, 1, 1]
            for num, sc in enumerate([score1, score2, score]):
                if sc != score:
                    path[num] = 0
            opened = True if score in (score1, score2) else False
            path_matrix[j][i] = ''.join([str(element) for element in path])
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
    unaligned_end_of_seq1 = first[i:]
    unaligned_end_of_seq2 = second[j:]
    if len(unaligned_end_of_seq1) >= len(unaligned_end_of_seq2):
        gaps_for_unaligned_seq1_minus_unaligned_seq2 = "-"*(len(unaligned_end_of_seq1)-len(unaligned_end_of_seq2))
        gaps_for_unaligned_seq2_minus_unaligned_seq_1 = ""
    else:
        gaps_for_unaligned_seq1_minus_unaligned_seq2 = ""
        gaps_for_unaligned_seq2_minus_unaligned_seq_1 = "-" * (len(unaligned_end_of_seq2)-len(unaligned_end_of_seq1))
    reversed_end_of_seq2 = str(unaligned_end_of_seq2 + gaps_for_unaligned_seq1_minus_unaligned_seq2)[::-1]
    reversed_end_of_seq1 = str(unaligned_end_of_seq1 + gaps_for_unaligned_seq2_minus_unaligned_seq_1)[::-1]

    alignment = [reversed_end_of_seq1, reversed_end_of_seq2]
    while score_matrix[j][i] != 0:
        diagonal = score_matrix[j - 1][i - 1]
        left = score_matrix[j][i - 1]
        up = score_matrix[j - 1][i]
        initial_vals = [left, up, diagonal]
        initiaL_dirs = ["left", "up", "diagonal"]
        path = [int(element) for element in list(path_matrix[j][i])]
        left_dirs = []
        left_vals = []
        for num, dir in enumerate(initiaL_dirs):
            if path[num]:
                left_dirs.append(dir)
                left_vals.append(initial_vals[num])
        #next_one = max(diagonal, left, up)
        next_one = max(left_vals)
        if diagonal == next_one and "diagonal" in left_dirs:
            alignment[0] += first[i-1]
            alignment[1] += second[j-1]
            i -= 1
            j -= 1
        elif left == next_one and "left" in left_dirs:
            alignment[0] += first[i-1]
            alignment[1] += "-"
            i-=1
        elif up == next_one and "right" in left_dirs:
            alignment[0] += "-"
            alignment[1] += second[j-1]
            j -= 1
    alignment[0] = alignment[0][::-1] # reverse the sequences
    alignment[1] = alignment[1][::-1]
    unaligned_start_of_seq1 = first[:i]
    unaligned_start_of_seq2 = second[:j]
    alignment[0] = unaligned_start_of_seq1 + alignment[0] # add unaligned start of reference.
    alignment[1] = unaligned_start_of_seq2 + alignment[1]
    if len(unaligned_start_of_seq1) >= len(unaligned_start_of_seq2):
        gaps_for_unaligned_seq1_minus_unaligned_seq2 = "-"*(len(unaligned_start_of_seq1)-len(unaligned_start_of_seq2))
        gaps_for_unaligned_seq2_minus_unaligned_seq1 = ""
    else:
        gaps_for_unaligned_seq1_minus_unaligned_seq2 = ""
        gaps_for_unaligned_seq2_minus_unaligned_seq1 = "-"*(len(unaligned_start_of_seq2)-len(unaligned_start_of_seq1))
    alignment[0] = gaps_for_unaligned_seq2_minus_unaligned_seq1 + alignment[0]
    alignment[1] = gaps_for_unaligned_seq1_minus_unaligned_seq2 + alignment[1]
    if len(alignment[0]) < len(alignment[1]):
        alignment[0] += "-" * (len(alignment[1])-len(alignment[0]))
    # add unaligned start of query. The construction is similar to one at the start of a loop - where I added
    # the unaligned end
    return max(numbers), "\n".join(alignment)


def merge_seqs(alignment):
    seq1, seq2 = alignment.split("\n")
    query = re.compile(r'^\-+')
    srch = lambda q, s: len(q.match(s).group(0)) if q.match(s) else 0
    len1start, len1end = srch(query, seq1), srch(query, seq1[::-1])
    len2start, len2end = srch(query, seq2), srch(query, seq2[::-1])
    result = ""
    if len1start and not len2start:
        result += seq2[:len1start]
        start = len1start
    else:
        result += seq1[:len2start]
        start = len2start
    if len1end and not len2end:
        result += seq2[start:]
    else:
        result += seq1[start:]

    return result


def Naive_assembler(file, threshold = 2):
    records = list(SeqIO.parse(file, format=file.split(".")[-1]))
    unable_to_merge = False
    while len(records) != 1 and unable_to_merge != True:
        print(len(records))
        i = 0
        for record in records:
            i +=1
            record.id = str(i)
        alignments = []
        for i, record1 in enumerate(records):
            for j, record2 in enumerate(records):
                if i >= j:
                    continue
                #print(record1.id, record2.id)
                score, alignment = local_align(str(record1.seq), str(record2.seq))
                alignments.append([score, alignment, record1, record2])
        alignments.sort(key= lambda element: element[0], reverse=True)
        records_merged = set()
        new_reads = []
        i = 0
        if alignments[i][0] < threshold:
            unable_to_merge = True
        for i in range(len(alignments)):
            if alignments[i][0] < threshold:
                break
            if records_merged.intersection(set([record.id for record in alignments[i][2:]])):
                continue
            new_reads.append(SeqIO.SeqRecord(id=str(i), seq=merge_seqs(alignments[i][1])))
            for element in alignments[i][2:]:
                records_merged.add(element.id)
        new_reads += [record for record in records if record.id not in records_merged]
        records = new_reads
    return records


def shotgun_sequencing(genome, mean_read_length, num_of_reads):
    reads = []
    for _ in range(num_of_reads):
        length = mean_read_length + np.random.randint(-int(mean_read_length*0.1), int(mean_read_length*0.1))
        start = np.random.randint(0, len(genome)-length)
        end = start + length
        reads.append(genome[start:end])
    return reads

def generate_genome(genome_length):
    genome = ""
    for i in range(genome_length):
        genome += np.random.choice(list("ATGC"))
    return genome

# genome = generate_genome(100)
# reads = shotgun_sequencing(genome, 10, 100)
# with open("simulated_reads.fasta", "w") as fl:
#     i = 1
#     for read in reads:
#         fl.write(f">{i}\n{read}\n")
#         i += 1
# with open("simulated_genome.fasta", "w") as fl:
#     fl.write(f">genome\n{genome}")

records = Naive_assembler("simulated_reads.fasta", 5)
with open("assembled_genome.fasta", "w") as fl:
    for record in records:
        fl.write(f'>{record.id}\n{record.seq}\n')
