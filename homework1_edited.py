import math
import operator

def first_task():
    print("Hello, Sasha! This is the first task. Enjoy watching.") # Ye, I did enjoy it)
    ints = list(range(1, 6)) # Not necessary to convert to list
    floats = [float(i) for i in ints]
    strings = [str(i) for i in ints]
    funcs = [int, float, str]
    lists = [ints, floats, strings]
    names = ["integer", "float", "string"]
    for i in range(3): # also you could use enumerate() to reduce number of loops
        for element in lists[i]:
            for func in funcs:
                if funcs.index(func) != i:
                    print("%s to %s" % (names[i], names[funcs.index(func)]))
                    print("{} -> {}".format(element, func(element)))

def second_task():
    print("Here is the second task. It contains Cosine theorem, malthusian growth equation and formula for \
    equilibrium frequency of allele under mutation-selecion balance")
    def cosine_theorem():
        print("This is a cosine theorem.")
        print("You need to type length of sides and size of the angle. You will get the size of an opposite side.")
        a = float(input("First side size: "))
        b = float(input("Second side size: "))
        alpha = float(input("Angle size: ")) # units should be specified (everywhere ideally))
        print("Size of an opposite side = ", (a**2+b**2 - 2*a*b*math.cos(alpha))**(0.5))
        print("\n")
    def malthusian_growth():
        print("This is a maltusian growth formula.")
        print("You need to type size of population at 0 point of time, malthusian parameter and time elapsed since \
        the 0 point. You will get the size of population at this point of time.")
        N0 = int(input("Population size at 0 time point: "))
        m = float(input("Malthusian parameter: "))
        t = float(input("Elapsed time: "))
        print("Population size at time t = ", N0*math.exp(m*t))
        print("\n")
    def mutation_selectuin_balance():
        print("This is a mutation-selection balance formula.")
        print("You need to type mutation rate and selection coefficient and you will get the equilibrium frequency of \
allele")
        mu = float(input("Mutation rate: "))
        s = float(input("Selection coefficient (greater than mutation rate): "))
        print("Equilibrium frequency = ", mu*(1-s)/s)
        print("\n")
    cosine_theorem()
    malthusian_growth()
    mutation_selectuin_balance()
    input("Press Enter to continue")


def third_task():
    def nor(x, y):
        return  not (x or y)
    def xor(x, y):
        return x and y
    def nand(x, y):
        return not (x and y)
    # def and_(x, y):
    #     return x and y
    # def or_(x, y):
    #     return x or y
    # def not_(x):
    #     return not x
    funcs = [operator.not_, operator.or_, operator.and_, nor, operator.xor, nand]
    names = ["not", "or", "and", "nor", "xor", "nand"]
    print("Welcome to the third task! Here you may see truth table of not, or, xor, and AND nand.")
    print("not:")
    print("Input\t\t\tOutput")
    for element in (True, False):
        print("%s\t\t\t%s" %(str(element), str(not(element))))
    print("-----------------")
    for q in range(1, len(funcs)): # here enumerate could also be used to get access to func and index simultaneously
        print(str(names[q]) + ":") # and zip to take name on each iteration
        print("Input\t\t\tOutput")
        for i in (True, False):
            for j in (True, False):
                print("%s\t%s\t|%s" % (str(i), str(j), str(funcs[q](i, j))))
        print("-----------------")
    input("Press Enter to continue")



def fourth_task():
    print("Here is the fourth task. It implements fizzbuzz program.")
    a = int(input("Enter an integer: "))
    x = "" # nice variant, though seems to me not the most performant
    if a % 3 == 0:
        x += "fizz"
    if a % 5 == 0:
        x += "buzz"
    print(x)

for element in (first_task, second_task, third_task, fourth_task):
    element()
    print("\n\n\n")

print("That's all, thanks for watching!") # You are welcome, thank you for homework)
