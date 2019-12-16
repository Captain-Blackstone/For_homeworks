"""
Hello, Sasha! Welcome to my last homework in this semester.
I passed to the Future Biotech winter retreat, by the way)
"""
from homework9 import shaker
import numpy as np
from Bio import SeqIO
from Bio.Seq import translate
def mapping_and_filtering():
    """
    Mapping and filtering examples
    :return: None
    """
    from_heroes = {"black dragon":7, "thunderbird":5, "swordsman":4, "imp":1, "dendroid":5, "lava element":5,
                   "pirate":3, "peasant":1, "stone golem":3, "lizardman":2, "death knight":6}
    from_starcraft = {"zergling":1, "vulture":2, "carrier":3, "zealot":1, "hydralisk":2, "science vessel":3, "defiler":3,
                      "marine":1, "dragoon":2}
    high_tier_sc = list(filter(lambda element: from_starcraft[element] == max(from_starcraft.values()),
                               from_starcraft.keys()))
    print(high_tier_sc)
    higher_tier_h = list(filter(lambda element: from_heroes[element]>from_starcraft[high_tier_sc[0]],
                                from_heroes.keys()))
    print(higher_tier_h)
    s_men = list(filter(lambda element: element[0]=="s", from_heroes.keys()))
    print(s_men)
    shaked = list(map(shaker, from_heroes.keys()))
    print(shaked)
    units = list(from_starcraft.keys()) + list(from_heroes.keys())
    np.random.shuffle(units)
    labeled = list(map(lambda element: "heroes" if element in from_heroes.keys() else "starcraft", units))
    print(labeled)
    random_units = list(map(lambda element: np.random.choice(list(from_starcraft.keys())) if element == "starcraft" else
                            np.random.choice(list(from_heroes.keys())), labeled))
    print(random_units)

def protein_generator(fasta, codon_table = "Standard"):
    """
    Yelds one protein sequence at a time from your fasta file
    :param fasta: path to fasta file
    :param codon_table: codon table used for translation
    """
    genes = SeqIO.parse(fasta, "fasta")
    for gene in genes:
        yield translate(gene.seq, table=codon_table)

mapping_and_filtering()
for seq in protein_generator("uc001skm.4.fasta"):
    print(seq)