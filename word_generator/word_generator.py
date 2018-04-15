"""Tools for creating words in constructed languages

Note: here 'y' is as in English, i.e. the glide IPA [j]
"""

import random
import csv
import os

CONSTRAINTS_DIR = os.path.join(os.curdir,"constraints")

# We're not worried about specific words yet, so just have indices for now
# TODO: load this from csv
DEFINITION_LIST = range(100)
# WORD_LIST = []

# This could be strings or functions
# TODO: load this from csv
MORPHEME_LIST = [


]

# Parts of speech
# TODO: load all these from csv
POS = [
    "noun",
    "verb",
    "adjective",
]

NOUN_PREFIXES = [
    ""
]

NOUN_SUFFIXES = [
    "ai",
    "in",
    "sim",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]

VERB_PREFIXES = [
    ""
]

VERB_SUFFIXES = [
    "ar",
    "al",
    "ir",
    "il",
    "or",
    "ol",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

ADJ_PREFIXES = [
    ""
]

ADJ_SUFFIXES = [
    ""
]

# function words, here used just for effect rather than for meaning
LITTLE_WORDS = [
"go","an","wa","so","te","heo"
]

PUNCTUATION = [
    ".",
    ",",
    "?",
    "!"
]

def load_phon_template(phon_csv):
    """Load phonology from csv"""
    with open(phon_csv) as source:
        reader = csv.DictReader(source)
        initials = list()
        medials = list()
        finals = list()
        for row in reader:
            if int(row["initial"]) == 1:
                initials.append(row["phoneme"])
            if int(row["medial"]) == 1:
                medials.append(row["phoneme"])
            if int(row["final"]) == 1:
                finals.append(row["phoneme"])
    return initials, medials, finals


def lenite(word):
    pass

def create_words(phon_csv,max_syls = 4):
    """Make words within constraints specified above"""
    initials, medials, finals = load_phon_template(phon_csv)
    created_words = set() # list of words
    defs_and_words = set() # list of (definition,word)
    # To ensure some variety, keep track of the prev word
    prev_initial = ""
    prev_medial = ""
    prev_final = ""
    cur_initial = ""
    cur_medial = ""
    cur_final = ""

    for definition in DEFINITION_LIST:
        word = None
        current_word_parts = list()
        while word is None or word in created_words:
            num_syls = random.randint(1,max_syls)
            for syl in range(num_syls):
                while cur_initial == prev_initial:
                    cur_initial = random.choice(initials)
                prev_initial = cur_initial
                current_word_parts.append(cur_initial)

                while cur_medial == prev_medial:
                    cur_medial = random.choice(medials)
                prev_medial = cur_medial
                current_word_parts.append(cur_medial)

                while cur_final == prev_final:
                    cur_final = random.choice(finals)
                prev_final = cur_final
                current_word_parts.append(cur_final)
            word = "".join(current_word_parts)
        created_words.add(word)
        defs_and_words.add((definition,word))
    return defs_and_words

def apply_morphology(word,pos):
    """Apply morphology to word"""
    word_conj = ""
    if pos == "noun":
        noun_prefix = random.choice(NOUN_PREFIXES)
        noun_suffix = random.choice(NOUN_SUFFIXES)
        word_conj = "{}{}{}".format(noun_prefix,word,noun_suffix)
    elif pos == "verb":
        verb_prefix = random.choice(VERB_PREFIXES)
        verb_suffix = random.choice(VERB_SUFFIXES)
        word_conj = "{}{}{}".format(verb_prefix,word,verb_suffix)

    elif pos == "adjective":
        adj_prefix = random.choice(ADJ_PREFIXES)
        adj_suffix = random.choice(ADJ_SUFFIXES)
        word_conj = "{}{}{}".format(adj_prefix,word,adj_suffix)
    else:
        word_conj = word
    return word_conj

def random_little_word(little_word_proportion):
    """Randomly add little words based on desired proportion"""
    little_word_choice = ""
    ints = range(10)
    matches = random.sample(ints,little_word_proportion)
    int_choice = random.randint(0,10)
    if int_choice in matches:
        little_word_choice = random.choice(LITTLE_WORDS)
    return little_word_choice

def create_fake_text(defs_and_words,num_sents=10,max_sent_length=8,little_word_proportion=3):
    """Create a fake text with no meaning"""
    text = list() # The created text
    words = [word for definition, word in defs_and_words]
    for sent_count in range(num_sents):
        current_sent = list()
        first_word = random.choice(words)
        first_pos = random.choice(POS)
        first_word_conj = apply_morphology(first_word,first_pos)
        prev_word = first_word
        prev_pos = first_pos
        cur_word = first_word
        cur_pos = first_pos
        current_sent.append(first_word_conj)
        little_word_choice = random_little_word(little_word_proportion)
        if little_word_choice != "":
            current_sent.append(little_word_choice)
        for word_count in range(max_sent_length):
            while cur_word == prev_word:
                cur_word = random.choice(words)
            while cur_pos == prev_pos:
                cur_pos = random.choice(POS)
            prev_word = cur_word
            prev_pos = cur_pos
            cur_word_conj = apply_morphology(cur_word,cur_pos)
            current_sent.append(cur_word_conj)
            little_word_choice = random_little_word(little_word_proportion)
            if little_word_choice != "":
                current_sent.append(little_word_choice)
        text.extend(current_sent)
        text.append(random.choice(PUNCTUATION))
    return " ".join(text)

if __name__ == "__main__":
    for lang_name, max_syl in [("lang01",3),("lang02",3),("lang03",1),("lang04",4)]:
        print("Creating language from {} template".format(lang_name))
        csv_name = "{}_template.csv".format(lang_name)
        filename = os.path.join(CONSTRAINTS_DIR,csv_name)
        defs_and_words = create_words(filename,max_syls=max_syl)
        for definition, word in defs_and_words:
            print("{}: {}".format(definition, word))
        print()
        print("Creating sample text:")
        fake_text = create_fake_text(defs_and_words)
        print(fake_text)
        print()
