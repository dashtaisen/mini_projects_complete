"""Tools for creating words in constructed languages

Note: here 'y' is as in English, i.e. the glide IPA [j]
"""

import random


# Include consonant clusters here
"""
POSSIBLE_INITIALS = [
    "p","t","k",
    "b","d","g",
    "f","s","h", #"š",
    #"v","z", #"ž",
    #"ts","tš",
    #"dz","ž",
    "m","n",
    "r","l","y",
    ""
]
"""

"""
POSSIBLE_INITIALS = [
    "p","t","k",
    "b","d","g",
    "f","s","h", "š",
    "v","z", "ž",
    "ts","tš",
    "dz","ž",
    "m","n",
    "r","l","y",
    ""
]
"""

"""
POSSIBLE_INITIALS = [
    "p","t","k",
    "pr","tr","kr",
    "pl","tl","kl",
    "py","ty","ky",
    "ps","pn","ks","kn",
    "b","d","g",
    "br","dr","gr",
    "bl","dl","gl",
    "by","dy","gy",
    "f","s","h", "š",
    "fr","sr","hr","šr",
    "fl","sl","hl","šl",
    "sy","hy","šy",
    "v","z", "ž",
    "vr","zr","žr",
    "vl","zl","žl",
    "vy","zy","žy",
    "ts","tš",
    "dz","dž",
    "m","n",
    "r","l","y",
    ""
]
"""

POSSIBLE_INITIALS = [
    "p","t","k",
    "v","h",
    "r","y"
]


POSSIBLE_MEDIALS = [
    "a","e","i","o","u",
    "ai","ao",
    "ea","ei","eu",
    "ia","ie","io","iu",
    "oi","ou",
    "ua","ui"
]

"""
POSSIBLE_FINALS = [
    #"f","s","š","h",
    "m","n",
    "r","l","y",
    ""
]
"""

"""
POSSIBLE_FINALS = [
    "f","s","š","h",
    "m","n",
    "r","l","y",
    ""
]
"""

"""
POSSIBLE_FINALS = [
    "p","t","k",
    "pr","tr","kr",
    "pl","tl","kl",
    "py","ty","ky",
    "ps","pn","ks","kn",
    "b","d","g",
    "br","dr","gr",
    "bl","dl","gl",
    "by","dy","gy",
    "f","s","h", "š",
    "fr","sr","hr","šr",
    "fl","sl","hl","šl",
    "sy","hy","šy",
    "v","z", "ž",
    "vr","zr","žr",
    "vl","zl","žl",
    "vy","zy","žy",
    "ts","tš",
    "dz","dž",
    "m","n",
    "r","l","y",
    ""
]
"""

POSSIBLE_FINALS = [
    "a","i","u"
]



# We're not worried about specific words yet, so just have indices for now
DEFINITION_LIST = range(100)
# WORD_LIST = []

# This could be strings or functions
MORPHEME_LIST = [


]

# Parts of speech
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

def lenite(word):
    pass

def create_words(max_syls = 4):
    """Make words within constraints specified above"""
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
                    cur_initial = random.choice(POSSIBLE_INITIALS)
                prev_initial = cur_initial
                current_word_parts.append(cur_initial)

                while cur_medial == prev_medial:
                    cur_medial = random.choice(POSSIBLE_MEDIALS)
                prev_medial = cur_medial
                current_word_parts.append(cur_medial)

                while cur_final == prev_final:
                    cur_final = random.choice(POSSIBLE_FINALS)
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
    defs_and_words = sorted(create_words(),key=lambda x:x[0])
    for definition, word in defs_and_words:
        print("{}: {}".format(definition, word))
    fake_text = create_fake_text(defs_and_words)
    print(fake_text)
