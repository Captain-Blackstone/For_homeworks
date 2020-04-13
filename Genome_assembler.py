import numpy as np
import networkx as nx
from collections import Counter
import os

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