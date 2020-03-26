"""
Hello, Sasha!
Wecome to my first homework in this semester. I am not tired yet, so I can be sightly creative gere ;)
"""
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations_with_replacement, product
from Bio import SeqIO
from Bio.Data import CodonTable

### Itertools part

def pile():
    values = [str(i) for i in range(2, 11)] + list("JDKA")
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    return list(product(values, suits))

def seqs_of_n(n):
    letters = "ATGC"
    for i in range(1, n+1):
        for element in product(*[letters]*i):
            yield "".join(element)

codons = CodonTable.unambiguous_dna_by_name["Standard"]


class DarkOverlord:
    """
    A class representing all Dark overlords of the universe.
    """
    goal = "Take over the world"

    def __init__(self, name, intelligence):
        self.name = name
        self.intelligence = intelligence
        self.succeeded = False

    def __str__(self):
        return f"Pleasure to meet you, sir. My name is {self.name} and my goal is to {DarkOverlord.goal.lower()}."

    def make_stupid_mistake(self, mistake):
        print(f"Although {self.name} had exceedingly high intelligence of {self.intelligence}, he made a huge mistake."
              f" He coudn't resist to {mistake[0].lower() + mistake[1:]}.")
        self.succeeded = False

    def declare_vengence_plans(self, target):
        print(f"Curse you, {target.name}! This is not our last meeting! I will be back and will {DarkOverlord.goal.lower()} the next time!")

    def achieve_success(self):
        self.succeeded = True
        print(f"I, {self.name}, managed to {DarkOverlord.goal}")

    def fail_to_achieve_success(self):
        self.succeeded = False


class RNAseq:
    letters = "AUGC"
    compound_class = "nucleic acid"

    def __init__(self, seq):
        self.seq = seq
        self.orf = None
        self.translate() # this is just to set self.orf


    def translate(self):
        aa_seq = ""
        start = False
        stop = False
        for i in range(len(self.seq)):
            codon = self.seq[i:i+3]
            if codon == "AUG":
                start = True
            if start:
                if codon in ("UAG", "UAA", "UGA"):
                    stop = True
                    break
                aa_seq += codons.forward_table[codon.replace("U", "T")]
        if start and stop:
            self.orf = True
        else:
            self.orf = False
        return aa_seq

    def reverse_transcription(self):
        input = "AUGC"
        output = "TACG"
        translation_table = str.maketrans(input, output)
        return str.translate(self.seq, translation_table)

class PositiveOnly(set):
    def __init__(self, args_tuple):
        super().__init__()
        for argument in args_tuple:
            self.add(argument)


    def add(self, object):
        if object > 0:
            super().add(object)

class Record:
    def __init__(self, name="", seq=""):
        self.name = name
        self.seq = seq
    def give_name(self, name):
        self.name = name
    def give_seq(self, seq):
        self.seq = seq

class FastaStatistics:
    def __init__(self, path):
        self.path = path
        self.records = []
        with open(path, "r") as fl:
            lines = fl.readlines()
        for line in lines:
            if line.startswith(">"):
                self.records.append(Record())
                self.records[-1].give_name(line[1:].strip())
            else:
                self.records[-1].give_seq(line.strip())


    def count_seqs(self):
        return len(self.records)

    def hist_lengths(self):
        lengths = [len(record.seq) for record in self.records]
        plt.hist(lengths, bins=len(lengths))
        plt.show()

    def gc_content(self):
        all_seqs = "".join([records.seq for records in self.records])
        return round((all_seqs.count("G") + all_seqs.count("C"))/len(all_seqs), 3)

    def hist_4mers(self):
        four_mers = ["".join(x) for x in product(*["ATGC"]*4)]
        counts = [sum([record.seq.count(four_mer) for record in self.records]) for four_mer in four_mers]
        fig = plt.figure()
        axes = fig.add_subplot()
        axes.hist(counts, bins=np.arange(len(four_mers))-0.5)
        axes.set_xticks(list(range(len(four_mers))))
        # print(list(range(len(four_mers))))
        axes.set_xticklabels(four_mers, rotation=90)
        plt.show()

    def __str__(self):
        print(self.path)

    def do_stats(self):
        print("number of seqs: ", self.count_seqs())
        print("GC-content: ", self.gc_content())
        self.hist_lengths()
        self.hist_4mers()

fasta = FastaStatistics("/home/dmitry/Diploma/Scripts/Compensatory_frameshifts/5_Conserved_Sequence/vertebrates/for_ancestor_reconstruction/fasta/uc002zwv.1.fasta")
fasta.do_stats()






Sauron = DarkOverlord(name="Sauron", intelligence=6)
Voldemort = DarkOverlord(name="Voldemort", intelligence=5)
BillCipher = DarkOverlord(name="Bill Cipher", intelligence=8)
print(Sauron)
print(Voldemort)
print(BillCipher)
Sauron.achieve_success()
BillCipher.achieve_success()
Sauron.fail_to_achieve_success()
Sauron.declare_vengence_plans(BillCipher)
BillCipher.make_stupid_mistake("Get into Stan's head")
Voldemort.achieve_success()
Voldemort.make_stupid_mistake("Kill Harry Potter")

my_rna = RNAseq("AUGUGGUGAUAA")
print(my_rna.translate())
print(my_rna.orf)

positiver = PositiveOnly((3, -1, 4, 5))
print(positiver)
positiver.add(-5)
positiver.add(10)
print(positiver)
