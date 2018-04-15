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
WORD_LIST_FNAME = os.path.join(CONSTRAINTS_DIR, "basic_word_list.csv")
# WORD_LIST = []

# Parts of speech
# TODO: load all these from csv
POS = [
    "noun",
    "verb",
    "adjective",
]

# function words, here used just for effect rather than for meaning
LITTLE_WORDS = [
"go","an","wa","so","te","heo"
]

PUNCTUATION = [".",","]

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

def create_words(phon_csv,wordlist_fname,max_syls = 4):
    """Make words within constraints specified above"""
    initials, medials, finals = load_phon_template(phon_csv)
    created_words = list() # list of words
    defs_words_tags = list() # list of (definition,word)
    # To ensure some variety, keep track of the prev word
    prev_initial = ""
    prev_medial = ""
    prev_final = ""
    cur_initial = ""
    cur_medial = ""
    cur_final = ""

    defs_and_tags = list()

    with open(wordlist_fname) as source:
        reader = csv.DictReader(source)
        for row in reader:
            defs_and_tags.append((row["Word"],row["POS"]))

    for definition,tag in defs_and_tags:
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
        created_words.append(word)
        defs_words_tags.append((definition,word,tag))
    return defs_words_tags

def create_morphemes(defs_words_tags, phon_csv,morph_csv,max_syls=1):
    """Create morphemes"""
    morphemes = list() # list of morphemes
    defs_and_morphemes = list() # list of (meaning,morpheme) tuples
    initials, medials, finals = load_phon_template(phon_csv)
    with open(morph_csv) as source:
        # Get the morphs that exist in the language
        reader = csv.DictReader(source)
        morph_meanings = list()
        for row in reader:
            if int(row['in_lang']) == 1:
                morph_meanings.append(row['morpheme'])
    existing_words = [word for definition, word,tag in defs_words_tags]

    # To ensure some variety, keep track of the prev word
    prev_initial = ""
    prev_medial = ""
    prev_final = ""
    cur_initial = ""
    cur_medial = ""
    cur_final = ""

    for morph_meaning in morph_meanings:
        morpheme = None
        current_morpheme_parts = list()
        while morpheme is None or morpheme in existing_words or morpheme in morphemes:
            num_syls = random.randint(0,max_syls)
            for syl in range(num_syls):
                while cur_initial == prev_initial:
                    cur_initial = random.choice(initials)
                prev_initial = cur_initial
                current_morpheme_parts.append(cur_initial)

                while cur_medial == prev_medial:
                    cur_medial = random.choice(medials)
                prev_medial = cur_medial
                current_morpheme_parts.append(cur_medial)

                while cur_final == prev_final:
                    cur_final = random.choice(finals)
                prev_final = cur_final
                current_morpheme_parts.append(cur_final)
            morpheme = "".join(current_morpheme_parts)
        morphemes.append(morpheme)
        defs_and_morphemes.append((morph_meaning,morpheme))
    return defs_and_morphemes

def write_language_template(defs_words_tags, defs_and_morphemes,dest_fname):
    with open(dest_fname,'w') as dest:
        dest.write("Meaning,Word,Tag\n")
        for definition, word, tag in defs_words_tags:
            dest.write("w_{},{},{}\n".format(definition,word,tag))
        for definition, morpheme in defs_and_morphemes:
            dest.write("{},{}\n".format(definition,morpheme))

def apply_morphology(word,word_def,pos,defs_and_morphemes):
    """Apply morphology to word"""
    word_conj = ""
    gloss = []
    if pos == "n":
        n_prefixes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("prep_")
        ]
        n_suffixes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("n_")
        ]
        preposition_likelihood = random.random()
        if preposition_likelihood > .8:
            prefix_def, noun_prefix = random.choice(n_prefixes)
        else:
            prefix_def, noun_prefix = (None, None)
        suffix_def, noun_suffix = random.choice(n_suffixes)
        if prefix_def is not None:
            gloss.append(prefix_def)
            gloss.append(word_def)
            gloss.append(suffix_def)
            word_conj = "{}-{}-{}".format(noun_prefix,word,noun_suffix)
        else:
            gloss.append(word_def)
            gloss.append(suffix_def)
            word_conj = "{}-{}".format(word,noun_suffix)

    elif pos == "v":
        verb_morphemes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("v_")
        ]
        agr = list()
        tense = list()
        aspect = list()
        other_v_suffix = list()
        for definition, morpheme in verb_morphemes:
            if "agr" in definition: agr.append((definition, morpheme))
            elif "aspect" in definition: aspect.append((definition, morpheme))
            elif "tense" in definition: tense.append((definition, morpheme))
            else: other_v_suffix.append((definition, morpheme))
        agr_def, v_agr = random.choice(agr)
        aspect_def, v_aspect = random.choice(aspect)
        tense_def, v_tense = random.choice(tense)
        suffix_def, v_suffix = random.choice(other_v_suffix)

        word_conj = "{}-{}-{}-{}".format(v_agr,v_aspect,word,v_tense,v_suffix)
        gloss.extend([agr_def.replace("agr_",""), aspect_def.replace("aspect_",""),
            word_def, tense_def.replace("tense_",""), suffix_def.split("_")[-1]])

    elif pos == "a":
        adj_morphemes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("a_")
        ]
        suffix_def, adj_suffix = random.choice(adj_morphemes)
        word_conj = "{}-{}".format(word,adj_suffix)
        gloss.append(word_def)
        gloss.append(suffix_def)
    else:
        word_conj = word
    return word_conj,gloss

def random_little_word(little_word_proportion):
    """Randomly add little words based on desired proportion"""
    little_word_choice = ""
    ints = range(10)
    matches = random.sample(ints,little_word_proportion)
    int_choice = random.randint(0,10)
    if int_choice in matches:
        little_word_choice = random.choice(LITTLE_WORDS)
    return little_word_choice

def create_real_text(lang_template,num_sents=10):
    text = list() # The created text
    translation = list()
    words = list()
    defs_and_morphemes = list()
    with open(lang_template) as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["Meaning"].startswith("w_"):
                words.append((row["Meaning"],row["Word"],row["Tag"]))
            else:
                defs_and_morphemes.append((row["Meaning"],row["Word"]))

    nouns = [
        word for word in words if word[2] == "n"
    ]

    verbs = [
        word for word in words if word[2] == "v"
    ]

    adjectives = [
        word for word in words if word[2] == "a"
    ]

    misc_words = [
        word for word in words if word[2] == "m"
    ]


    for sent_count in range(num_sents):
        current_sent = list()
        obj = random.choice(nouns)
        obj_def = obj[0].replace("w_","")
        obj_word = obj[1].replace("n_","")
        obj_tag = obj[2]

        adj = random.choice(adjectives)
        adj_def = adj[0].replace("w_","")
        adj_word = adj[1].replace("a_","")
        adj_tag = adj[2]

        verb = random.choice(verbs)
        verb_def = verb[0].replace("w_","")
        verb_word = verb[1].replace("v_","")
        verb_tag = verb[2]

        obj_conj,gloss = apply_morphology(obj_word,obj_def,obj_tag,defs_and_morphemes)
        obj_gloss = "-".join([item for item in gloss])

        adj_conj,gloss = apply_morphology(adj_word,adj_def,adj_tag,defs_and_morphemes)
        adj_gloss = "-".join([item for item in gloss])

        verb_conj,gloss = apply_morphology(verb_word,verb_def,verb_tag,defs_and_morphemes)
        verb_gloss = "-".join([item for item in gloss])

        verb_def_gloss = verb_gloss.replace("v_","")
        adj_def_gloss = adj_gloss.replace("a_","")
        obj_def_gloss = obj_gloss.replace("n_","")

        current_sent = [verb_conj, obj_conj, adj_conj]
        current_translation = [verb_def_gloss, obj_def_gloss, adj_def_gloss]
        text.extend(current_sent)
        translation.extend(current_translation)
        punct = random.choice(PUNCTUATION)
        text.append(punct)
        translation.append(punct)

    return " ".join(text), " ".join(translation)


def create_fake_text(lang_template,num_sents=10,max_sent_length=8,little_word_proportion=3):
    """Create a fake text with no meaning"""
    text = list() # The created text
    words = list()
    defs_and_morphemes = list()
    with open(lang_template) as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["Meaning"].startswith("w_"):
                words.append((row["Word"],row["Tag"]))
            else:
                defs_and_morphemes.append((row["Meaning"],row["Word"]))
    for sent_count in range(num_sents):
        current_sent = list()
        first_word,first_pos = random.choice(words)
        first_word_conj = apply_morphology(first_word,first_pos,defs_and_morphemes)
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
                cur_word,cur_pos = random.choice(words)
            prev_word = cur_word
            prev_pos = cur_pos
            cur_word_conj = apply_morphology(cur_word,cur_pos,defs_and_morphemes)
            current_sent.append(cur_word_conj)
            little_word_choice = random_little_word(little_word_proportion)
            if little_word_choice != "":
                current_sent.append(little_word_choice)
        text.extend(current_sent)
        text.append(random.choice(PUNCTUATION))
    return " ".join(text)


if __name__ == "__main__":

    for lang_name, max_syl in [("lang01",3)]:#("lang02",3),("lang03",1),("lang04",4)]:
        print("Creating language from {} template".format(lang_name))
        phon_csv = "{}_phonology.csv".format(lang_name)
        morph_csv = "{}_morphology.csv".format(lang_name)
        phon_filename = os.path.join(CONSTRAINTS_DIR,phon_csv)
        morph_filename = os.path.join(CONSTRAINTS_DIR,morph_csv)
        defs_words_tags = create_words(phon_filename,WORD_LIST_FNAME,max_syls=max_syl)
        for definition, word,tag in defs_words_tags:
            print("{}: {} ({})".format(definition, word,tag))
        print()

        print("Creating morphemes:")
        defs_and_morphemes = create_morphemes(defs_words_tags, phon_filename,morph_filename,max_syls=1)
        for definition, morpheme in defs_and_morphemes:
            print("{}: {}".format(definition, morpheme))
        print()



    print("Writing language template:")
    template_fname = os.path.join(CONSTRAINTS_DIR,"{}_template.csv".format(lang_name))
    write_language_template(defs_words_tags,defs_and_morphemes,template_fname)


    print("Creating sample text:")
    #fake_text = create_fake_text(os.path.join(CONSTRAINTS_DIR,"lang01_template.csv"))
    #print(fake_text)
    #print()

    text, trans = create_real_text(template_fname)
    text_sents = text.split(".")
    trans_sents = trans.split(".")
    for i in range(len(text_sents)):
        print(text_sents[i])
        print()
        print(trans_sents[i])
        print()
    print()
