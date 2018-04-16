"""Tools for creating words in constructed languages

How to run:

Look at lang01_mophology and lang01_phonology, and wordlist csv files,
to see how the constraints are set up

You can also look at lang03. lang02 and lang04 aren't done yet.

To run on the lang01 templates, just run at the command line:

python word_generator.py

To create your own templates:
1. Add to the wordlist as you like
2. Create your own phonology and morphology files from the templates
3. Change the LANG_NAME and MAX_SYL at the top of this file
LANG_NAME should correspond to the filename of your phonology/morphology files
MAX_SYL is the maximum syllable lengths of words in your language

Then run python word_generator.py from the command line.
"""

import random
import csv
import os

# Name of the language in the phonology and morphology templates
LANG_NAME = "lang01"

#Max syllables of words in the language
MAX_SYL = 3


# The directory with the various phonological and morphological constraints
CONSTRAINTS_DIR = os.path.join(os.curdir,"constraints")

# DEFINITION_LIST if we're just making up random words
DEFINITION_LIST = range(100)

# Actual word list
WORD_LIST_FNAME = os.path.join(CONSTRAINTS_DIR, "basic_word_list.csv")

PUNCTUATION = [".",","]

def load_phon_template(phon_csv):
    """Load phonology from template csv
    Input:
        phon_csv: csv of phonological rules
    Returns:
        initials, medials, finals: lists of phonemes for each position
    """
    with open(phon_csv) as source:
        """phon_csv should have the following columns:
        phoneme: the phoneme
        initial: whether it can be in initial position (0 or 1)
        medial: whether it can be in medial position (0 or 1)
        final: whether it can be in final position (0 or 1)
        """
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
    """Apply lenition to a word"""
    pass

def create_words(phon_csv,word_csv,max_syls = 4):
    """Make words within constraints
    Inputs:
        phon_csv: csv of phonological constraints
        word_csv: csv of words and their parts of speech
        max_syls: max syls per word
    Returns:
        defs_words_tags: list of (definition, word, postag) tuples
    """
    initials, medials, finals = load_phon_template(phon_csv)
    created_words = list() # list of words
    defs_words_tags = list() # list of (definition,word,tag)

    # To ensure some variety, keep track of the prev word
    prev_initial = ""
    prev_medial = ""
    prev_final = ""
    cur_initial = ""
    cur_medial = ""
    cur_final = ""

    defs_and_tags = list()

    # Get the definitions and tags from the word list
    with open(word_csv) as source:
        reader = csv.DictReader(source)
        for row in reader:
            defs_and_tags.append((row["Word"],row["POS"]))

    # Create the words
    for definition,tag in defs_and_tags:
        word = None
        current_word_parts = list()

        # Loop to avoid homophones
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
    """Create morphemes
    Inputs:
        defs_words_tags: list of (definition,word,pos) that we created
        phon_csv: csv of phonological cosntraints
        morph_csv: csv of morphemes that exist in the language
        max_syls: max syl length of morpheme
    """
    morphemes = list() # list of morphemes
    defs_and_morphemes = list() # list of (meaning,morpheme) tuples
    initials, medials, finals = load_phon_template(phon_csv)

    # Get the morphemes that exist in the language
    with open(morph_csv) as source:
        reader = csv.DictReader(source)
        morph_meanings = list()
        for row in reader:
            if int(row['in_lang']) == 1:
                morph_meanings.append(row['morpheme'])

    # Get list of existing words to avoid homophones
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

        # Loop to avoid homophones
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
    """Write list of words and morphemes to a template csv"""
    with open(dest_fname,'w') as dest:
        dest.write("Meaning,Word,Tag\n")
        for definition, word, tag in defs_words_tags:
            dest.write("w_{},{},{}\n".format(definition,word,tag))
        for definition, morpheme in defs_and_morphemes:
            dest.write("{},{}\n".format(definition,morpheme))

def apply_morphology(word,word_def,pos,defs_and_morphemes):
    """Apply morphology to word
    Inputs:
        word: the word itself (in the target language)
        word_def: word definition in English
        pos: postag of the word
        defs_and_morphemes: list of (meaning,morpheme) tuples
    Returns:
        word_conj: conjugated form of the word
        gloss: meanings of the word and its morphemes
    """
    # TODO: move defs_and_morphemes out of here to save time

    # Conjugated form of the word, with morphology applied
    word_conj = ""

    # English definition of the word and its morphemes
    gloss = []

    """Based on POS, get the relevant morphemes,
        add them to the word, and get the gloss too"""

    if pos == "time":
        time_postpositions = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("prep_") and "time" in definition
        ]
        time_def, time_morph = random.choice(time_postpositions)
        gloss.append(word_def)
        # Split at _ and take the last item to just get the prep meaning
        gloss.append(time_def.split("_")[-1])
        word_conj = "{}-{}".format(word,time_morph)

    elif pos == "loc":
        loc_postpositions = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("prep_") and "loc" in definition
        ]
        loc_def, loc_morph = random.choice(loc_postpositions)
        gloss.append(word_def)
        # Split at _ and take the last item to just get the prep meaning
        gloss.append(loc_def.split("_")[-1])
        word_conj = "{}-{}".format(word,loc_morph)

    elif pos == "n":
        n_prefixes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("prep_") and "loc" not in definition and "time" not in definition
        ]
        n_suffixes = [
            (definition, morpheme) for definition, morpheme in defs_and_morphemes
            if definition.startswith("n_")
        ]

        # Only add a preposition 20% of the time
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

    # If the POS is something completely different
    else:
        word_conj = word

    return word_conj,gloss

def create_text(lang_template,num_sents=10):
    """Create a text based on the language template
    Inputs:
        lang_template: template csv
        num_sents: number of sentences
    Returns:
        text
        gloss
    """
    text = list() # The created text
    gloss = list()

    words = list()
    defs_and_morphemes = list()

    # Get the words and morphemes
    with open(lang_template) as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["Meaning"].startswith("w_"):
                words.append((row["Meaning"],row["Word"],row["Tag"]))
            else:
                defs_and_morphemes.append((row["Meaning"],row["Word"]))

    # Get the words for each part of speech
    # TODO: do this in less code

    nouns = [
        word for word in words if word[2] == "n"
    ]
    verbs = [
        word for word in words if word[2] == "v"
    ]
    adjectives = [
        word for word in words if word[2] == "a"
    ]
    determiners = [
        word for word in words if word[2] == "det"
    ]
    conjunctions = [
        word for word in words if word[2] == "conj"
    ]
    times = [
        word for word in words if word[2] == "time"
    ]
    locations = [
        word for word in words if word[2] == "loc"
    ]


    # Create the sentences
    # TODO: do this in less code

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

        time = random.choice(times)
        time_def = time[0].replace("w_","")
        time_word = time[1].replace("time_","")
        time_tag = time[2]

        loc = random.choice(locations)
        loc_def = loc[0].replace("w_","")
        loc_word = loc[1].replace("loc_","")
        loc_tag = loc[2]

        # Conjugate, get glosses, and remove tags such as w_ and a_
        # TODO: less code, better code
        obj_conj,obj_gloss = apply_morphology(obj_word,obj_def,obj_tag,defs_and_morphemes)
        obj_gloss_string = "-".join([item for item in obj_gloss]).replace("n_","")

        adj_conj,adj_gloss = apply_morphology(adj_word,adj_def,adj_tag,defs_and_morphemes)
        adj_gloss_string = "-".join([item for item in adj_gloss]).replace("a_","")

        verb_conj,verb_gloss = apply_morphology(verb_word,verb_def,verb_tag,defs_and_morphemes)
        verb_gloss_string = "-".join([item for item in verb_gloss]).replace("v_","")

        time_conj,time_gloss = apply_morphology(time_word,time_def,time_tag,defs_and_morphemes)
        time_gloss_string = "-".join([item for item in time_gloss]).replace("time_","")

        loc_conj,loc_gloss = apply_morphology(loc_word,loc_def,loc_tag,defs_and_morphemes)
        loc_gloss_string = "-".join([item for item in loc_gloss]).replace("loc_","")

        current_sent = [time_conj, loc_conj, obj_conj, adj_conj, verb_conj]
        current_gloss = [
                    time_gloss_string, loc_gloss_string,
                    obj_gloss_string, adj_gloss_string, verb_gloss_string
        ]
        text.extend(current_sent)
        gloss.extend(current_gloss)
        punct = random.choice(PUNCTUATION)
        text.append(punct)
        gloss.append(punct)

    return " ".join(text), " ".join(gloss)


if __name__ == "__main__":
    
    print("Creating language from {} template".format(LANG_NAME))
    phon_csv = "{}_phonology.csv".format(LANG_NAME)
    morph_csv = "{}_morphology.csv".format(LANG_NAME)
    phon_filename = os.path.join(CONSTRAINTS_DIR,phon_csv)
    morph_filename = os.path.join(CONSTRAINTS_DIR,morph_csv)
    defs_words_tags = create_words(phon_filename,WORD_LIST_FNAME,max_syls=MAX_SYL)
    for definition, word,tag in defs_words_tags:
        print("{}: {} ({})".format(definition, word,tag))
    print()

    print("Creating morphemes:")
    defs_and_morphemes = create_morphemes(defs_words_tags, phon_filename,morph_filename,max_syls=1)
    for definition, morpheme in defs_and_morphemes:
        print("{}: {}".format(definition, morpheme))
    print()


    print("Writing language template:")
    template_fname = os.path.join(CONSTRAINTS_DIR,"{}_template.csv".format(LANG_NAME))
    write_language_template(defs_words_tags,defs_and_morphemes,template_fname)


    #template_fname = os.path.join(CONSTRAINTS_DIR,"{}_template_saved.csv".format(LANG_NAME))

    print("Creating sample text:")
    text, trans = create_text(template_fname)
    text_sents = text.split(".")
    trans_sents = trans.split(".")
    for i in range(len(text_sents)):
        print(text_sents[i])
        print()
        print(trans_sents[i])
        print()
    print()
