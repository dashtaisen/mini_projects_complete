from string import punctuation

"""
Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
"""

def name_value(name):
    return sum([(ord(char) - 64) for char in name])

def sort_names(namefile):
    with open("names.txt") as f:
        raw = f.read()
        names = sorted([name for name in raw.split(",")])
    return names

def get_namesum(namefile):
    names = sort_names(namefile)
    namesum = 0
    for name_index in range(len(names)):
        #Don't need to convert to uppercase for this dataset, but could need for other datasets
        name = names[name_index].strip(punctuation).upper()
        score = name_value(name) * (name_index + 1)
        namesum += score
        #print("{}: {}".format(name, score))
    return namesum

if __name__ == "__main__":
    print(get_namesum('./names.txt'))
