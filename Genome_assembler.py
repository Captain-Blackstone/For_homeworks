import numpy as np
import networkx as nx
from homework4 import flatten
from collections import Counter
import os

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


def generate_genome(genome_length):
    genome = ""
    for i in range(genome_length):
        genome += np.random.choice(list("ATGC"))
    return genome

def shotgun_sequencing(genome, mean_read_length, num_of_reads):
    """
    Errors happen with rate 0.001
    :param genome: genome to sequence
    :param mean_read_length: mean read length of your sequenator. You'll get reads in range 0.9mrl - 1.1mrl
    :param num_of_reads: number of reads you want to get.
    :return: list of your reads
    """
    reads = []
    for _ in range(num_of_reads):
        length = mean_read_length + np.random.randint(-int(mean_read_length*0.1), int(mean_read_length*0.1))
        start = np.random.randint(0, len(genome)-length)
        end = start + length
        read = list(genome[start:end])
        numbers = [0 for _ in range(999)] + [1]
        for position in range(len(read)):
            number = np.random.choice(numbers)
            if number:
                read[position] = np.random.choice(list(set(list("ATGC")).difference(set([read[position]]))))
        reads.append("".join(read))
    return reads

def extract_kmers(reads, k):
    kmers = list()
    for read in reads:
        for i in range(len(read)-k+1):
            kmer = read[i:i+k]
            kmers.append(kmer)
    return kmers

def generate_de_bruijn_graph(kmers):
    graph = nx.MultiDiGraph()
    for kmer in kmers:
        graph.add_edge(kmer[:-1], kmer[1:])
    return graph

def process_de_bruijn_graph(graph):
    edges = graph.edges
    edges = [(edge[0], edge[1]) for edge in edges]
    edges = list(set(edges))
    froms = [edge[0] for edge in edges]
    candidates = [node for node in froms if froms.count(node) == 1]
    falses = set()
    k = len(candidates[0]) + 1
    while len(candidates) != 0:
        candidate = candidates[0]
        to = list(filter(lambda el: el[0] == candidate, edges))[0][1]
        tos = [edge[0] for edge in edges]
        if tos.count(to) != 1:
            falses.add(candidate)
        # if len(graph.nodes) > 2:
        graph = collapse_edge(graph, candidate, to, k)
        # elif len(graph.nodes) == 2:
        #     return graph
        edges = graph.edges
        edges = [(edge[0], edge[1]) for edge in edges]
        edges = list(set(edges))
        print(len(edges))
        froms = [edge[0] for edge in edges]
        candidates = list({node for node in froms if froms.count(node) == 1}.difference(falses))
    return graph

def cut_off_tips(graph, k):
    edges = list(graph.edges)
    if edges:
        candidate = edges[0][0]
    else:
        candidate = None
    false = set()
    while candidate:
        print("here")
        edges_of_interest = list(filter(lambda el: el[0] == candidate, edges))
        edges_of_interest = [(el[0], el[1]) for el in edges_of_interest]
        c = Counter(edges_of_interest)
        pair_of_interest = None
        for pair in c.keys():
            if c[pair] == max(c.values()) and list(c.values()).count(max(c.values())) == 1:
                pair_of_interest = pair
        if pair_of_interest:
            graph = collapse_edge(graph, pair_of_interest[0], pair_of_interest[1], k)
        else:
            false.add(candidate)
        edges = list(graph.edges)
        possible_candidates = {edge[0] for edge in edges}.difference(false)
        if possible_candidates:
            candidate = list(possible_candidates)[0]
        else:
            candidate = None
    return graph

def collapse_edge(graph, node1, node2, k):
    new_graph = nx.MultiDiGraph()
    new_node = node1[:-(k-2)] + node2
    current_edges = graph.edges
    current_nodes = set(graph.nodes)
    new_neighbours_from = [edge[0] for edge in current_edges if edge[1] == node1]
    new_neighbours_to = [edge[1] for edge in current_edges if edge[0] == node2]
    new_graph.add_node(new_node)
    for node in new_neighbours_from:
        new_graph.add_edge(node, new_node)
    for node in new_neighbours_to:
        new_graph.add_edge(new_node, node)
    nodes_to_add = current_nodes.difference({node1, node2}).difference(set(new_graph.nodes))
    for node in nodes_to_add:
        new_graph.add_node(node)
    new_edges = [edge for edge in current_edges if not {node1, node2}.intersection(set(edge))]
    for edge in new_edges:
        new_graph.add_edge(edge[0], edge[1])
    return new_graph

def assembler(reads, k=30):
    kmers = extract_kmers(reads, k)
    graph = generate_de_bruijn_graph(kmers)
    graph = process_de_bruijn_graph(graph)
    graph = cut_off_tips(graph, k=30)
    nx.nx_pydot.write_dot(graph, 'graph.dot')
    os.system("dot -Tpng graph.dot > graph.png")
    os.system("rm graph.dot")
    contigs = list(graph.nodes)
    with open("Assembled_genome_de_bruijn.txt", "w") as fl:
        i = 0
        for contig in contigs:
            i += 1
            fl.write(f">{i}\n{contig}\n")
    print(f"Congradulations! Your genome is assembled. {len(contigs)} contigs were generated.")


### TEST ###

genome = generate_genome(1000)
with open("simulated_genome.fasta", "w") as fl:
    fl.write(f">genome\n{genome}")

reads = shotgun_sequencing(genome, 100, 100)
with open("simulated_reads.fasta", "w") as fl:
    i = 1
    for read in reads:
        fl.write(f">{i}\n{read}\n")
        i += 1

assembler(reads)