import random
import matplotlib.pyplot as plt
print(""" In case you've become interested in this file. I wrote an article on a Biomolecule site
(here it is - https://biomolecula.ru/articles/kak-poniat-chto-vashi-geny-otbiraiut)
And I am very curious, weather it is actually popular or not. Well, to measure that you could simply look at the number 
of watchers. But I invented more pleasing metrics - that is number of users added my article to favirites divided by 
number of watchers. Why I like this metrics? Because it says, that my article is better than others... Yes, I am pretty
concerned about this...
Anyways. I want to know what is the probability of observing that my article is better by this parameter by chance? 
I probably could use statistics for that, but I decided to walk an easy way - bootstrap. And here it is.
""")

MY_WATCHERS = 487
MY_FAVORITES = 7

def comparator(their_favorites, their_watchers):
    y1 = [0 for i in range(40)]
    y2 = [0 for i in range(40)]
    who_is_better = [0, 0]
    for i in range(1000):
        print("%i/1000" % i)
        f = 0
        for j in range(MY_WATCHERS):
            a = random.randint(1, MY_WATCHERS)
            if a <= MY_FAVORITES:
                f += 1
        y1[f] += 1
        g = 0
        for j in range(their_watchers):
            a = random.randint(1, their_watchers)
            if a <= their_favorites:
                g += 1
        y2[g] += 1
        if f > g:
            who_is_better[0] += 1
        elif f < g:
            who_is_better[1] += 1
    print("Probability of being better: ", who_is_better[0]/(who_is_better[0]+who_is_better[1]))
    plt.bar(range(40), y1, color="red", alpha=0.5, label="my")
    plt.bar(range(40), y2, color="blue", alpha=0.5, label="theirs")
    plt.legend()
    plt.show()

comparator(5, 1298)