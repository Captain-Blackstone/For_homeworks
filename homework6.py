import networkx as nx
import matplotlib.pyplot as plt
from homework4 import flatten
print("""Hello, Sasha! Welcome to my 6th homework. Unfortunately, I do it while listening to a very irritating lecture 
from my professor about why he doesn't want to do his job. So there probably won't be any jokes =|""")

def importers():
    """
    Creates 2 files: one of them imports the other. Returns nothing.
    :return: Nothing, I said.
    """
    with open("importer.py", "w") as importer, open("imported.py", "w") as imported:
        imported.write("print('Hello, I am imported!')")
        importer.write("print('Looks like I have imported some file')")

def copying_function(input, output, start=0, finish=None):
    """
    Copies some amount of text from one file to another (all the text by default)
    :param input: input file (with path)
    :param output: output file (with path)
    :param start: int - number of line you want to start with
    :param finish: int - number of line you want to finish on
    :return: nothing
    """
    with open(input, "r") as i, open(output, "w") as o:
        content = i.readlines()
        if not finish:
            finish = len(content)
        content = content[start:finish]
        for line in content:
            o.write(line)

def graph_drawing(graph_list):
    graph = nx.Graph()
    for key in graph_list.keys():
        for node in graph_list[key]:
            graph.add_edge(key, node)
    nx.draw_shell(graph, with_labels=True)
    plt.show()

def components_of_connectedness(graph_list):
    """
    gives you number of components of connectedness of given graph
    :param graph_list: graph in a form of graph list
    :return: number of components of connectedness
    """
    detected = {}
    current_component = 0
    for node in graph_list.keys(): # walk through all the nodes
        if node not in flatten(detected.values()): # if havent' seen that node previously (= found new component)
            current_component += 1 # register a component
            detected[current_component] = [node] # add node to "seen"
            nodes_to_check = graph_list[node]
            while len(nodes_to_check) > 0: # walk through this node's neighbours and their neighbours and so on.
                current = nodes_to_check[-1]
                detected[current_component].append(current)
                for every in graph_list[current]:
                    if every not in detected[current_component] and every not in nodes_to_check:
                        nodes_to_check.append(every)
                nodes_to_check.remove(current)
    return current_component


gr_list = dict(tavern = ["university", "magic_guild", "market"], university = ["tavern", "blacksmiths"], magic_guild=["tavern"],
               blacksmiths=["university"], market=["tavern"], castle=["armory"], armory=["castle"], guild_of_thieves=["cave"],
               cave=["guild_of_thieves"])
graph_drawing(gr_list)

print(components_of_connectedness(gr_list))