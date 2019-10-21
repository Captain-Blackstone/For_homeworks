import random
def the_lone_task():
    print("Hello, Sasha! Looks like I've already done most of this homework. That's why, unfortunately, I won't be "
          "able to entertain you for long. Enjoy this lone task.")
    strongest = dict()
    strongest["Castle"] = 'Archangel'
    strongest["Rampart"] = "Golden Dragon"
    strongest["Tower"] = "Titan"
    strongest["Inferno"] = "Arch Devil"
    strongest["Necropolis"] = "Ghost Dragon"
    strongest["Dungeon"] = "Black Dragon"
    strongest["Stronghold"] = "Ancient Behemoth"
    strongest["Fortress"] = "Chaos Hydra"
    strongest["Conflux"] = "Foenix"
    strongest["Cove"] = "Haspid"
    strongest.pop("Conflux") # They often ban conflux =(
    print("Hey, I always wondered, who is stronger, %s or %s?" % (strongest["Dungeon"], strongest["Rampart"]))
    print("Let's give those creatures fuuny names")
    for key, value in strongest.items():
        name = ""
        for letter in value:
            name += letter * random.randint(1, 5)
        name = " ".join(name.split()) # Don't want to have many spaces
        print(key, name)

the_lone_task()