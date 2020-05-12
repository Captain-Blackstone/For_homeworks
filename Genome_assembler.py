import argparse
import numpy as np
import networkx as nx
import logging
from collections import Counter
import os
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")
    assemble = subparsers.add_parser(name="assemble")
    assemble.add_argument("-i", "--input",
                        required=True,
                        type=str,
                        help="Input file with reads in fasta or fastq format.")
    #reads = [str(read.seq) for read in SeqIO.parse("xxx", format=file_with_reads.split(".")[-1])]
    #mean_read_length = int(np.mean(np.array([len(read) for read in reads])))
    assemble.add_argument("-o", "--output",
                        required=True,
                        type=str,
                        help="Output file.")
    assemble.add_argument("-k", "--KmerLength",
                        default=30,
                        type=int,
                        help="Length of k-mers that will be used in assembly.")
    simulate = subparsers.add_parser(name="simulate")
    simulate.add_argument("-s", "--GenomeSize",
                                default=10000,
                                type=int,
                                help="Size of genome to be simulated.")
    simulate.add_argument("-n", "--NumberOfReads",
                                default=1000,
                                type=int,
                                help="Number of reads to be simulated.")
    simulate.add_argument("-l", "--MeanReadLength",
                                default=100,
                                type=int,
                                help="Mean length of simulated reads.")
    simulate.add_argument("-og", "--OutputGenome",
                                default="Simulated_genome.fasta",
                                type=str,
                                help="File where simulated genome goes.")
    simulate.add_argument("-or", "--OutputReads",
                                default="Simulated_reads.fasta",
                                type=str,
                                help="File where simulated reads go.")
    args = parser.parse_args()
    if args.mode == "assemble":
        logging.basicConfig(filename=f"{args.input.split('.')[0]}_assembly.log",
                            filemode="w",
                            format="%(message)s",
                            level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        assembler(file_with_reads=args.input, output_file=args.output, k=args.KmerLength, logger=logger)
    elif args.mode == "simulate":
        logging.basicConfig(filename=f"{args.input.split('.')[0]}_simulation.log",
                            filemode="w",
                            format="%(message)s",
                            level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info("Generating genome...")
        genome = generate_genome(args.GenomeSize)
        with open(args.OutputGenome, "w") as fl:
            fl.write(f">genome\n{genome}")
        logger.info("Running shotgun sequence...")
        reads = shotgun_sequencing(genome,args.MeanReadLength, args.NumberOfReads)
        with open(args.OutputReads, "w") as fl:
            i = 1
            for read in reads:
                fl.write(f">{i}\n{read}\n")
                i += 1
        logger.info("Simulation complete.")



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

def extract_kmers(reads, k, logger):
    kmers = list()
    mean_length = int(np.mean(np.array([len(read) for read in reads])))
    if k > mean_length:
        logger.warning(f"Warning. Your k (or default k=30) is not optimal. Mean read length is {mean_length}")
        new_k = int(mean_length*0.8)
        logger.info(f"Prooceeding with k = {new_k}")
        return new_k
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

def process_de_bruijn_graph(graph, logger):
    edges = graph.edges
    edges = [(edge[0], edge[1]) for edge in edges]
    edges = list(set(edges))
    froms = [edge[0] for edge in edges]
    candidates = [node for node in froms if froms.count(node) == 1]
    if not candidates:
        return graph
    falses = set()
    k = len(candidates[0]) + 1
    sum_of_progression = len(candidates)/0.37
    i_threshold = sum_of_progression*0.05
    current_work_done = 0
    while len(candidates) != 0:
        pairs_to_collapse = []
        untouchable = []
        i = 0
        for candidate in candidates:
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
            i += 1
            if i > i_threshold:
                current_work_done += 5
                logger.info(current_work_done, "%")
                i = 0

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
    if current_work_done < 100:
        logger.info("100 %")
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

def assembler(file_with_reads, output_file, k, logger):
    reads = [str(read.seq) for read in SeqIO.parse(file_with_reads, format=file_with_reads.split(".")[-1])]
    logger.info("Extracting k-mers...")
    kmers = extract_kmers(reads, k, logger)
    if type(kmers) == int:
        k = kmers
        logger.info(f"Extracting k-mers with k = {k}")
        kmers = extract_kmers(reads, k, logger)
    logger.info("Done")
    graph = generate_de_bruijn_graph(kmers)
    logger.info("Processing graph...")
    graph = process_de_bruijn_graph(graph, logger)
    logger.info("Done")
    logger.info("Cutting off tips...")
    graph = cut_off_tips(graph, k=30)
    logger.info("Done")
    nx.nx_pydot.write_dot(graph, 'graph.dot')
    os.system(f"dot -Tpng graph.dot > {file_with_reads.split('.')[0]}.png")
    os.system("rm graph.dot")
    contigs = list(graph.nodes)
    with open(output_file, "w") as fl:
        i = 0
        for contig in contigs:
            i += 1
            fl.write(f">{i}\n{contig}\n")
    logger.info(f"Congradulations! Your genome is assembled. {len(contigs)} contigs were generated.")


### TEST ###


# assembler("unknown_harder.fasta", 30)
if __name__ == "__main__":
    main()