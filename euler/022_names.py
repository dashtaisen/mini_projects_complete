"""
Nicholas A Miller
27 October 2017

Problem 022

Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
"""

from string import punctuation

def name_value(name):
    """Get name value: sum of char values of all-uppercased name
    Inputs:
        name: name, as a string
    Returns:
        name value: as int
    """
    #64 is char val of A, hard-coded for speed since it'll never change
    #Preformat names at this step too
    return sum([(ord(char) - 64) for char in name.strip(punctuation).upper()])

def sort_names(namefile):
    """Sort names alphabetically
    Inputs:
        namefile: path of file containing names, as string
    Returns:
        names: list of names
    """
    with open("names.txt") as f:
        raw = f.read()
        names = sorted([name for name in raw.split(",")])
    return names

def get_namesum(namefile):
    """Get total name sum: name values * indices
    Inputs:
        namefile: path of file containing names, as string
    Returns:
        namesum: total score
    """
    names = sort_names(namefile)
    namesum = 0
    for name_index in range(len(names)):
        name = names[name_index]
        score = name_value(name) * (name_index + 1)
        namesum += score
        #print("{}: {}".format(name, score))
    return namesum

if __name__ == "__main__":
    namesum = get_namesum('./names.txt')
    assert namesum == 871198282 #Test that it works
    print(namesum)
    print("OK!")
