"""
Hello, Sasha! In case you're interested in this file, here is a description.
There are two similar phenomena in evolutionary genomics: genetic hitchhiking (you probably know, what it is, but still
here is a link - https://en.wikipedia.org/wiki/Genetic_hitchhiking) and background selection
(this one you probably don't know - https://en.wikipedia.org/wiki/Background_selection/). The former is fixation of neutral
or slightly deleterious mutation located closely on chromosome with an advantageous one (the recombination has limited
rate). The latter is 'death' of neutral or slightly advantageous mutation located closely on chromosome with a
deleterious one (both effects take place because of limited recombination rate, so fates of closely located mutations
become linked).
It is commonly inferred, that background selection may be a reason of local decrease of diversity in genome. And this
is what I cannot understand.
What is diversity?  It is quite intuitive. If there is only one allele in the locus, then diversity is extremely low.
If we consider two alleles in the locus, diversity is maximum if their frequencies are equal (0.5:0.5), and minimum when
one of them is rare and the other is nearly fixated (like 0.9999:0.0001).
See, if mutation is deleterious, it will soon disappear. In the limit case it is lethal
and will disappear in the first generation it appeared. So, if we look from the perspective of an allele in nearby
locus, it has some chance of gaining lethal mutation near it and die with it together. In other words, background
selection is very similar to random death of certain copies. If we have frequencies 0.9999:0.0001 and if we know, that
approximately one lethal mutation per generation happens in nearby locus, then this mutation will cause decrease of
diversity with probability 0.0001 (if it will kill the rare mutant) and increase diversity with probability 0.9999! So,
in that case, it looks like background selection should promote diversity, not lower it. But we probably should consider
amount of increase and decrease - if we have 1 mutant and 999 non-mutants, we will dramatically decrease diversity by
killing this mutant, but just slightly increase it if we kill one of 999 non-mutants.
So, it looks like quite a complicated problem for me. And the first step towards understanding this diversity-decreasing
conclusion everyone makes is modelling. Do I really see decrease of diversity with background selecton under my
assumptions?
To measure that I consider two models. One of them is a simple Wright-Fisher population - a model for studying genetic
drift (here are more details about it - https://en.wikipedia.org/wiki/Genetic_drift#Wright.E2.80.93Fisher_model).
In this model you have a population of size N every generation. And the only rule of generating those generation is as
follows: every member of population has an equal chance of being a parent of every offspring. Well, that may be not very
easy if you're not familiar with that concept. If you're interested, ask me later.
The second model is the same Wright-Fisher population but with background selection - that means that each generation
some number of random members of population die (as it aquired a lethal mutation and consequently wasn't able to be a
parent of any offspring).
What I want to gain is probability distribution of having k mutants in next generation if we have n mutants in current
generation? If ths distribution for background selection is located to the left from the same distribution for model
without background selection, then the common opinioin is correct - background selection decreases diversity. Is not -
well, there is something to think about...
"""

import matplotlib.pyplot as plt


def CisNpoK(n, k):
    n_fact = 1 # well, actually, it will be n!/(n-k)!
    for i in range(n-k+1, n+1):
        n_fact *= i
    k_fact = 1 # and this will be honest k!
    for i in range(1, k+1):
        k_fact *= i
    return int(n_fact/k_fact) # which is n!/[k!(n-k)!]

def pmf(now, next, N):
    """
    This is actually Bernoulli formula with n = N, k = next, p = now/N.
    But the goal of such representation is to put this formula in Wright-Fisher population representation. So it
    calculates the probability of observing "next" mutants in next generation if "now" mutants are present in current
    generation. N is population size.
    :param now: int - number of mutants in current generation
    :param next: int - number of mutants in next generation
    :param N: population size
    :return: probability of observing "next" mutants in next generation giver "now" mutants in current generation
    """
    return CisNpoK(N, next)*((now/N)**next)*((1 - now/N)**(N-next))

def pmf_background(n, N, k, m):
    """
    This function models background selection in one generation. See, background selection can be represented as random
    killing of members of population - you just think they gained a lethal mutation and died, and since this mutation
    knows nothing about genotype of the animal, it looks like death of random member of population.
    UPD. I was very surprised to see that I derived the formula of hypergeometric distribution here.
    https://en.wikipedia.org/wiki/Hypergeometric_distribution
    And, of course, I was very proud of myself.
    :param n: int - number of mutants in the population
    :param N: int - population size
    :param k: int - number of mutants who will die due to background selection.
    :param m: int - number of animals who will die due to background selection. Something like lethal mutation rate.
    :return: probability of k mutants dying, given population of size N, where n mutants are present and background
    selection removes m animals each generation
    """
    res = CisNpoK(m, k)
    for i in range(n-k+1, n+1):
        res *= i
    for i in range(N-n-(m-k)+1, N-n+1):
        res *= i
    for i in range(N-m+1, N+1):
        res /= i
    return res

def drift_background(now, N, m, next):
    """
    This one calculates probability of having "next" mutants in next generation, having "now" mutants in current
    generation taking into account background selection with rate m
    :param now: int - number of mutants in current generation
    :param N: int - population size
    :param m: int - number of animals who will die due to background selection
    :param next: int - number of mutants in next generation
    :return: probability (see desctiption)
    """
    result = 0
    for k in range(min(now+1, m+1)):
        result += pmf(now-k, next, N-m)*pmf_background(now, N, k, m) # probability of observing "next" mutants in next generation
    return result

# def main(now, N, m):

y_drift = []
y_background = []
x = range(101)
now = 70
N = 100
m = 10
for i in range(N+1):
    y_background.append(drift_background(now, N, m, i))
    y_drift.append(pmf(now,  i, N))
plt.plot(x, y_drift, color="red", alpha=0.5, label="drift")
plt.plot(x, y_background, color="blue", alpha=0.5, label="drift+background")
plt.legend()
plt.show()