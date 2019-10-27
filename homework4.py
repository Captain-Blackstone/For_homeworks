from collections import Counter
# Hello, Sasha! Welcome to my next homework! Have you missed them? Well, sorry, this one doesn't contain
# jokes in any considerable amount. Those tasks just look like they are not jokable.


def flatten(lst):
    """
    Removes all the collections from the list, making their elements parts of the "global" list. Yes, it's an awful
    description.
    :param lst: list - a list you want to flatten. Boy, this description is astonishing.
    :return: list - a list without collections in it.
    """
    result = []
    for element in lst:
        try:  # To be honest, this looks like cheat since we haven't learned it yet.
            # If there's more elegant way, tell me, please
            result += element
        except TypeError:
            result.append(element)
    return result


def fibo(num):
    """
    calculates a Fibonacci number of specified number. Oh, come on. I mean, you specify the position, and the function
    gives you a number from Fibonacci series on that position. No, I give up. Hope you understand what this does.
    :param num: this aforementioned number/position. NB: counting from 0.
    :return: a number from Fibonacci series
    """
    if num < 0:
        return 0
    elif num < 2:
        return 1
    else:
        return fibo(num -1) + fibo(num - 2)


def maximum(lst):
    """
    This function returns an element of maximum value from list. Looks like I finally made a satisfying description.
    Hurray.
    :param lst: list - well, this aforementioned list
    :return: maximum number
    """
    result = lst[0]
    for element in lst:
        if element > result:
            result = element
    return result


def reverse(lst):
    """
    Returns a list in reversed order. This wasn't even difficult.
    :param lst: list - not surprisingly, a list, whivh you want to revert
    :return: reversed list
    """
    return lst[::-1] # Yes, it was a difficult one.


def mean(lst):
    """
    Returns a mean of a list. Do I even need to make a description for such functions?
    :param lst: list - guess what
    :return: mean
    """
    i = 0
    res = 0
    for element in lst:
        i += 1
        res += element
    return res/i


def moda(lst):
    """
    Returns the most frequent element(s) of list.
    :param lst: list - list
    :return: moda - the most frequent element(s)
    """
    # Warning. This doesn't seem to be elegant at all.
    c = Counter(lst)
    mx = maximum(list(c.values()))
    modes = []
    for key in c.keys():
        if c[key] == mx:
            modes.append(key)
    return tuple(modes)


def get(lst, ind):
    """
    Gets you an element from the list with specified index.
    :param lst: list - aforementioned list
    :param ind: int - aforementioned index. Boy, the word 'aforementioned' came in pretty handy.
    :return: the element with specified index
    """
    return lst[ind] # Too simple, no?





