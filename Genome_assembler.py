import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import os
from Bio import SeqIO

def flatten(lst):
    """
    Removes all the collections from the list, making their elements parts of the "global" list. Yes, it's an awful
    description.
    :param lst: list - a list you want to flatten. Boy, this description is astonishing.
    :return: list - a list without collections in it.
    """
    result = []
    contains_list = False
    for element in lst:
        if type(element) in (list, tuple):  # To be honest, this looks like cheat since we haven't learned it yet.
            # If there's more elegant way, tell me, please
            result += element
            contains_list = True
        else:
            result.append(element)
    if contains_list:
        return flatten(result)
    else:
        return result


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
    mean_length = int(np.mean(np.array([len(read) for read in reads])))
    if k > mean_length:
        print(f"Warning. Your k is not optimal. Mean read length is {mean_length}")
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
    if not candidates:
        return graph
    falses = set()
    k = len(candidates[0]) + 1
    while len(candidates) != 0:
        print(len(candidates), "candidates")
        pairs_to_collapse = []
        untouchable = []
        # candidate = candidates[0]
        iii = 0
        for candidate in candidates:
            # iii += 1
            # if not iii % 50:
            #     print(iii)
            to = list(filter(lambda el: el[0] == candidate, edges))[0][1]
            tos = [edge[1] for edge in edges]
            if tos.count(to) != 1:
                falses.add(candidate)
                continue
            if to not in untouchable and candidate not in untouchable:
                pairs_to_collapse.append((candidate, to))
                additional_untouchable = [candidate, to]
                additional_untouchable += [element[0] for element in filter(lambda el: el[1] == candidate, edges)]
                additional_untouchable += [element[1] for element in filter(lambda el: el[0] == to, edges)]
                untouchable += additional_untouchable
                untouchable = list(set(untouchable))
        ### This is for step-by-step visualisation. Green nodes - to be merged, red ones - not to be merged (untouchable) blue ones - never will be merged.
        # color_map = []
        # for node in graph:
        #     if node in flatten(pairs_to_collapse):
        #         color_map.append("green")
        #     elif node in untouchable:
        #         color_map.append("red")
        #     else:
        #         color_map.append("blue")
        # nx.draw(graph, node_color=color_map, with_labels=True)
        # plt.show()
        graph = collapse_edges(graph, pairs_to_collapse, k)
        edges = graph.edges
        edges = [(edge[0], edge[1]) for edge in edges]
        edges = list(set(edges))
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
    possible_candidates = {edge[0] for edge in edges}.difference(false)
    while candidate:
        untouchable = []
        pairs_to_collapse = []
        for candidate in possible_candidates:
            edges_of_interest = list(filter(lambda el: el[0] == candidate, edges))
            edges_of_interest = [(el[0], el[1]) for el in edges_of_interest]
            c = Counter(edges_of_interest)
            pair_of_interest = None
            for pair in c.keys():
                if c[pair] == max(c.values()) and list(c.values()).count(max(c.values())) == 1:
                    pair_of_interest = pair
            if pair_of_interest:
                if not set(pair_of_interest).intersection(set(untouchable)):
                    pairs_to_collapse.append(pair_of_interest)
                    additional_untouchable = list(pair_of_interest)
                    additional_untouchable += [element[0] for element in filter(lambda el: el[1] == pair_of_interest[0], edges)]
                    additional_untouchable += [element[1] for element in filter(lambda el: el[0] == pair_of_interest[1], edges)]
                    additional_untouchable += [element[1] for element in filter(lambda el: el[0] == pair_of_interest[0], edges)]
                    additional_untouchable += [element[0] for element in filter(lambda el: el[1] == pair_of_interest[1], edges)]
                    untouchable += additional_untouchable
                    untouchable = list(set(untouchable))
            else:
                print(candidate)
                false.add(candidate)
        ### Another visualization block
        # color_map = []
        # for node in graph:
        #     if node in flatten(pairs_to_collapse):
        #         color_map.append("green")
        #     elif node in untouchable:
        #         color_map.append("red")
        #     else:
        #         color_map.append("blue")
        # nx.draw(graph, node_color=color_map, with_labels=True)
        # plt.show()
        graph = collapse_edges(graph, pairs_to_collapse, k)
        edges = list(graph.edges)
        possible_candidates = {edge[0] for edge in edges}.difference(false)
        if possible_candidates:
            candidate = list(possible_candidates)[0]
        else:
            candidate = None
    return graph

def collapse_edges(graph, pairs, k):
    current_edges = graph.edges
    current_nodes = set(graph.nodes)
    new_graph = nx.MultiDiGraph()
    for pair in pairs:
        node1 = pair[0]
        node2 = pair[1]
        new_node = node1[:-(k-2)] + node2
        new_neighbours_from = [edge[0] for edge in current_edges if edge[1] == node1]
        new_neighbours_to = [edge[1] for edge in current_edges if edge[0] == node2]
        new_graph.add_node(new_node)
        for node in new_neighbours_from:
            new_graph.add_edge(node, new_node)
        for node in new_neighbours_to:
            new_graph.add_edge(new_node, node)
    nonexistent_nodes = set(flatten(pairs))
    nodes_to_add = current_nodes.difference(nonexistent_nodes).difference(set(new_graph.nodes))
    for node in nodes_to_add:
        new_graph.add_node(node)
    new_edges = [edge for edge in current_edges if not nonexistent_nodes.intersection(set(edge))]
    for edge in new_edges:
        new_graph.add_edge(edge[0], edge[1])
    return new_graph

def assembler(file_with_reads, k=30):
    reads = [str(read.seq) for read in SeqIO.parse(file_with_reads, format=file_with_reads.split(".")[-1])]
    kmers = extract_kmers(reads, k)
    graph = generate_de_bruijn_graph(kmers)
    graph = process_de_bruijn_graph(graph)
    graph = cut_off_tips(graph, k=30)
    nx.nx_pydot.write_dot(graph, 'graph.dot')
    os.system("dot -Tpng graph.dot > graph.png")
    os.system("rm graph.dot")
    contigs = list(graph.nodes)
    with open("Unknown_assembled.fasta", "w") as fl:
        i = 0
        for contig in contigs:
            i += 1
            fl.write(f">{i}\n{contig}\n")
    print(f"Congradulations! Your genome is assembled. {len(contigs)} contigs were generated.")


### TEST ###

# genome = generate_genome(100)
# with open("simulated_genome.fasta", "w") as fl:
#     fl.write(f">genome\n{genome}")

# reads = shotgun_sequencing(genome, 10, 100)
# with open("simulated_reads.fasta", "w") as fl:
#     i = 1
#     for read in reads:
#         fl.write(f">{i}\n{read}\n")
#         i += 1
assembler("unknown_harder.fasta", 30)