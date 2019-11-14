print("Hello, Sasha! Welcome to my 5th homework. This one will contain more Heroes of Might and Magic stuff if I'll be"
      "crafty enough...")

castles = ["Castle", "Rampart", "Necropolis", "Dungeon", "Tower", "Inferno",  "Stronghold", "Fortress", "Cove",
           "Conflux"]

tmpl_1 = 'A {} can kill {} of {}'
print(tmpl_1.format("balck dragon", "infinity", "peasants"))
print(tmpl_1.format("unicorn", "0", "black dragons"))
print("But! " + tmpl_1.format("unicorn", "infinity", "archangels") + " if gets very lucky!")
templ_2 = 'You would never choose {} over {}'
print(templ_2.format("scouting", "logistics"))
print(templ_2.format("sorcery", "earth magic"))
print(templ_2.format("heroes 5", "heroes 3"))
n = 1.6
templ_3 = f"{castles[0]} produces {round(n)}-fold less units of 7-th level than {castles[-1]}. So they should be ' \
          f'{round(n)}-fold better, shouldn't they?"
print(templ_3)
print("Here is a castle list:")
for element in castles:
    print("%10s" % element, end="")

boring, sisters_favourite, *other, imba = castles
*last_ones, no_magic_suckers_1, no_magic_suckers_2 = other
my_girlfriends_favourite, my_fathers_favouite, *tower_and_inferno = last_ones

# comprehensions

squares = [x**2 for x in range(11)]
sums = [x+y for x in range(3) for y in range(5, 9)]
nucleotides = ["A", "T", "G", "C"]
mutations = [f"{nucl_1}->{nucl_2}" for nucl_1 in nucleotides for nucl_2 in nucleotides if nucl_1 != nucl_2]
# Well, I can't build a matrix 3x3 with numbers from 0 to 9, because 3x3 = 9 and there are 10 numbers from 0 to 9...
matrix = [[i for i in range(j-2, j+1)] for j in range(3, 10, 3)]


def linear_search(element, lst):
    """
    implementation of linear search
    :param element: element you want to find
    :param lst: list, where you want to find it
    :return: True if element in list, else False
    """
    for i in range(len(lst)):
        if lst[i] == element:
            return i

def binary_search(element, lst):
    """
    implementation of binary search
    :param element: int or float - element you want to find
    :param lst: list, where you want to find it. Should consist of numbers!
    :return: element index in list, if not present - None
    """
    lst.sort()
    upper_bound = len(lst) -1
    lower_bound = 0
    previous_target = None
    while True:
        target = int((upper_bound+lower_bound)/2) # middle of a list that's left
        if lst[target] > element: # if element is smaller, get rid of the bigger half
            upper_bound = target
        elif lst[target] < element: # if bigger - get rid of the smaller half
            lower_bound = target
        else:
            return target # if equal - then found
        if target == previous_target: # if bounds don't shift anymore - we've reached the end
            break
        previous_target = target
    if lst[upper_bound] == element: # Not elegant. But couldn't create anything better. That thing shows up because of
        # rounding problem
        return upper_bound
