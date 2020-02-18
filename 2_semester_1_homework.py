"""
Hello, Sasha!
Wecome to my first homework in this semester. I am not tired yet, so I can be sightly creative gere ;)
"""

"Found this dictionary here: https://gist.github.com/stepjue/b2e957215f4e5121fa14"
codons = {
"UUU" : "F",
"CUU" : "L",
"AUU" : "I",
"GUU" : "V",
"UUC" : "F",
"CUC" : "L",
"AUC" : "I",
"GUC" : "V",
"UUA" : "L",
"CUA" : "L",
"AUA" : "I",
"GUA" : "V",
"UUG" : "L",
"CUG" : "L",
"AUG" : "M",
"GUG" : "V",
"UCU" : "S",
"CCU" : "P",
"ACU" : "T",
"GCU" : "A",
"UCC" : "S",
"CCC" : "P",
"ACC" : "T",
"GCC" : "A",
"UCA" : "S",
"CCA" : "P",
"ACA" : "T",
"GCA" : "A",
"UCG" : "S",
"CCG" : "P",
"ACG" : "T",
"GCG" : "A",
"UAU" : "Y",
"CAU" : "H",
"AAU" : "N",
"GAU" : "D",
"UAC" : "Y",
"CAC" : "H",
"AAC" : "N",
"GAC" : "D",
"UAA" : "Stop",
"CAA" : "Q",
"AAA" : "K",
"GAA" : "E",
"UAG" : "Stop",
"CAG" : "Q",
"AAG" : "K",
"GAG" : "E",
"UGU" : "C",
"CGU" : "R",
"AGU" : "S",
"GGU" : "G",
"UGC" : "C",
"CGC" : "R",
"AGC" : "S",
"GGC" : "G",
"UGA" : "Stop",
"CGA" : "R",
"AGA" : "R",
"GGA" : "G",
"UGG" : "W",
"CGG" : "R",
"AGG" : "R",
"GGG" : "G"
}


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
                aa_seq += codons[codon]
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