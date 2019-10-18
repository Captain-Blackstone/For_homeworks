def first_task():
    print("Good evening, Sasha! Welcome to my second homework."
          " I will do my best to make it as enjoyable, as the previous one\n And here is the first task.\n")
    protoss_units = []
    for unit in (bool("zealot"), "dragoon", "high templar", "dark templar"):
        protoss_units.append(unit)
    stargate_units = ["corsair", "scout", "carrier"]
    protoss_units.extend(stargate_units)
    protoss_units.remove("scout") # Nobody uses scouts
    protoss_units[1] = 10
    print("Where are my zealots? Only %i left!" % protoss_units.count("zealot")) # Unfortunately, I needed to convert zealot
    # to True in order to satisfy 'different types' condition, so there is no such entry
    print("My army consists of %i units now" % len(protoss_units))


def second_task():
    print("Here is the second task. Well, it is not as interesting as the prevoius one.")
    # We can't create an empty tuple and add a few elements, so I will create a full tuple right away.
    zerg_units = ("mutalisk", "mutalisk", "mutalisk", "mutalisk", "mutalisk", "mutalisk", "mutalisk", "mutalisk",
                  "overlord", not bool("queen")) # because you need an overlord to make mutastack.
    print("What a strange unit on the %ith slot of my army?" % zerg_units.index(False))
    print("I have %i units in mutastack. That's, probably, enough to push." % zerg_units.count("mutalisk"))
    print("My army consists of %i units. And one of them is False..." % len(zerg_units))


def third_task():
    terran_units = set()
    for unit in ("marine", "medic", bool("firebat"), "ghost", "vulture", "siege tank", "goliaph"):
        terran_units.add(unit)
    starport_units = {"wraith", "science vessel", "battle cruiser", "valkyrie"}
    terran_units = terran_units.union(starport_units)
    print(terran_units)
    terran_units.remove("ghost") # Nobody uses ghosts. With little exceptions.
    # There is no element with index 1, because there no indexes in sets.
    # So, I can't set an element with index 1 to be 10
    print("I have quite a small army now - %i units" % len(terran_units))
    if starport_units.issubset(terran_units):
        print("Looks like I have a little air support.")
    barracks_units = {"marine", "medic", "firebat", "ghost"}
    print("Starport units are totally different from barracks units. Their intersection is %i"
          % len(barracks_units.intersection(starport_units)))
    print("If all my bio units die, I will be left with ", terran_units.difference(barracks_units))
    first_army = {"marine", "medic", "siege tank"}
    second_army = {"vulture", "siege tank", "goliaph"}
    print("Unique units in our armies are ", first_army.symmetric_difference(second_army))


def fourth_task():
    print("And here is the fourth task. It looks better than previous ones.")
    string = input("Enter a string and I'll tell you everything about it: ")
    first_upper = "upper" if string[0].isupper() else "lower"
    cond = " " if string[-2:] == "!!" else " not "
    firecount = string.count("fire")
    upper = string.upper()
    lower = string.lower()
    title = string.title()
    print("First letter is in %s case" % first_upper)
    print("String does%sends with !!" % cond)
    print("Sring contains %i 'fire' substrings" % firecount)
    print("String in upper case - %s" % upper)
    print("String in lower case - %s" % lower)
    print("String with words starting with upper case letter - %s" % title)


def fifth_task():
    print("The fifth task. And I've run out of my imagination in creating intros. Sorry for that.")
    letter = input("Enter a string and you'll get some extremely useful information about it: ")[0]
    result = None
    if letter.isalpha():
        result = "letter"
    elif letter.isdigit():
        result = "number"
    elif letter.isspace():
        result = "space"
    print("Here is what you wanted to know! Your string starts with a %s." % result)


def sixth_task():
    print("Well, this one looks pretty much the same as the first one in the first homework. I improved a little :)")
    lst = list((range(1, 6)))
    tpl = tuple(lst)
    st = set(lst)
    string = "".join([str(el) for el in lst])
    funcs = [list, tuple, set]
    collections = [lst, tpl, st, string]
    names = ["list", "tuple", "set", "string"]
    for i, element in enumerate(collections):
        for func in funcs:
            if funcs.index(func) != i:
                print("%s to %s" % (names[i], names[funcs.index(func)]))
                print("{} -> {}".format(element, func(element)))


def seventh_task():
    print("We're almost there. This is the last one.")
    friends = ["Jim", "Sarah", "Arcturus"]
    for friend in friends + ["everyone!"]:
        print("Hi, %s" % friend)


def eightth_task():
    print("Oops. Haven't noticed the rest of them. Looks like there are quite a bit more... Here is the eightth.")
    print("This one will take 3 sides of a triangle and return its type.")
    sides = []
    for element in ("first", "second", "third"):
        sides.append(float(input("Enter the %s side size: " % element)))
    exists = True
    for side in sides:
        if 2*side >= sum(sides):
            exists = False
    if not exists:
        print("It's not a triangle, sorry.")
        return None
    sides = set(sides)
    if len(sides) == 1:
        res = "equilateral"
    elif len(sides) == 2:
        res = "isosceles"
    else:
        res = "miscellanious"
    print("Your triangle is %s" % res)


def ninegth_task():
    print("Oh. I'm already a little tired.")
    string = "Palindrom"
    lst = [letter for letter in string]
    print("first way")
    print(string[::-1])
    print(lst[::-1])
    print("second way")
    x = ""
    for letter in string:
        x = letter + x
    print(x)
    x = []
    for element in lst:
        x.insert(0, element)
    print(x)


def tenth_task():
    print("Tenth task. Reversecomplementator.")
    DNA = "ATTGTCTGATCTTAGTGC"
    print("First way")
    compl = {"A":"T", "T":"A", "C":"G", "G":"C"}
    reversecomplement = "".join([compl[letter] for letter in DNA][::-1])
    print(reversecomplement)
    print("Second way. May be not very different from the previous one. You may not score me points for that one :)")
    reversecomplement = ""
    for letter in DNA[::-1]:
        reversecomplement += compl[letter]
    print(reversecomplement)


def eleventh_task():
    print("And now we're almost there. Sum of even numbers in list.")
    lst = list(range(100))
    func = lambda i: i if i%2 == 0 else 0
    output = sum([func(i) for i in lst])
    print(output)
    print("And we are done.")


def missed_task():
    print("Not yet! Turns out, I missed one task. Here is is.")
    lst1 = [3, 6, 7, 8, 2, 58, 3, 575, 3]
    lst2 = [6, 3, 2, 83, 7, 3, 7, 3, 333]
    res = []
    for i in range(len(lst1)):
        res.append(lst1[i] + lst2[i])
    print(res)

for task in (first_task, second_task, third_task, fourth_task, fifth_task, sixth_task, seventh_task, eightth_task,
             ninegth_task, tenth_task, eleventh_task, missed_task):
    task()
    print("\n\n")