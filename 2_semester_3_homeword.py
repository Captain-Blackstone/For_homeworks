import re
import matplotlib.pyplot as plt
import urllib.request
from collections import Counter

def finder(text, pattern):
    """
    Just a helper function.
    :param text: text where to find
    :param pattern: pattern which you need to find
    :return: finditer generator
    """
    query = re.compile(pattern)
    results = query.finditer(text)
    return results

def ftp_finder(text):
    pattern = r"(ftp\..*?)[;\s]"
    return finder(text, pattern)

def digits_finder(text):
    pattern = r"\b\d+\b"
    return finder(text, pattern)

def a_words_finder(text):
    pattern = r"\b\w*[aA]\w*\b"
    return finder(text, pattern)

def exclamations_finder(text):
    pattern = r'((^)|([\.\?!] )|(\"))([^\.\?\"\']*?!)'
    return finder(text, pattern)

def length_dist(text):
    pattern = r"\w+"
    query = re.compile(pattern)
    search_res = query.findall(text)
    search_res = [len(word) for word in search_res]
    counter = Counter(search_res)
    labels = []
    values = []
    for key in counter.keys(): # i could have done smth like values = counter.values(), but I'm not sure they would be in the right order
        labels.append(key)
        values.append(counter[key])
    plt.bar(labels, values)
    plt.bar(labels, values)
    plt.show()

def e_mail_finder(text):
    pattern = r"\w+\@[a-z]+\.[a-z]{2,3}"
    return finder(text, pattern)

def printer(text, some_finder, description):
    """
    Another helper hunction
    :param text: text some_finder works on
    :param some_finder: one of my finder functions
    :return: None
    """
    print(description)
    for every in some_finder(text):
        print(every.group(0))
    print("-----")


references = "https://raw.githubusercontent.com/Serfentum/bf_course/master/15.re/references"
text = urllib.request.urlopen(references)
text = "\n".join([line.decode() for line in text])
with open("ftps", "w") as fl:
    for link in ftp_finder(text):
        fl.write(link.group(1) + "\n")
story = "https://raw.githubusercontent.com/Serfentum/bf_course/master/15.re/2430AD"
text = urllib.request.urlopen(story)
text = "\n".join([line.decode() for line in text])
printer(text, digits_finder, "Numbers")
printer(text, a_words_finder, "Words containing letter 'a'")
print("Exclamative sentences")
for every in exclamations_finder(text): # I gave up. For whatever reason it doesn't want to match ! xxxx! pattern.
    print(every.group(5))
print("-----")
printer(text, e_mail_finder, "emails")
length_dist(text)