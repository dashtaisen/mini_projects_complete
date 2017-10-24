# -*- coding: utf-8 -*-
"""
Script for preprocessing student notes.

@author: Nicholas A Miller
"""

import csv,re

class StudentNotePreprocessor:
    def __init__(self, abbrevs_path, collocations_path, assignments_path, headings_path):
        self.abbrevs = self.load_abbreviations(abbrevs_path)
        self.collocations = self.load_collocations(collocations_path)
        self.hw_cat, self.test_cat = self.load_assignments(assignments_path)
        self.headings = self.load_headings(headings_path)

    def load_headings(self, headings_path):
        return [line.strip() for line in open(headings_path).readlines()]

    def load_abbreviations(self, abbrevs_path):
        """Load abbreviations from csv into a dict
        Args:
            dict_path (str): path to the csv
        Returns:
            dict
        """
        abbrevs = dict()
        with open(abbrevs_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                abbrevs[row["abbreviation"]] = row["expansion"]
        return abbrevs

    def load_collocations(self,source_path):
        """Load collocations from a text file
        Args:
            source_path (str): path to txt
        Returns:
            set
        """
        with open(source_path) as f:
            collocations = [line.strip() for line in f]
        return set(collocations)

    def load_assignments(self, source_path):
        """Get assignment list from file
        Args:
            source_path (str)
        Returns:
            None
        """
        with open(source_path) as f:
            hw_cat = dict() #{hw: cat}
            test_cat = dict() #{test cat}
            reader = csv.DictReader(f)
            for row in reader:
                hw_cat[row["hw"]] = row["cat"]
                test_cat[row["test"]] = row["cat"]
            return hw_cat, test_cat

    def join_headings(self, text):
        """Join headings with an underscore
        We need this preprocessing step because many headings consist of more than one word,
        But we want to iterate by tokens,
        So we need to join the headings somehow to make them into tokens.
        """
        #Sorted so the longer ones subsume the shorter ones
        headings = sorted(self.headings, key= lambda x:len(x), reverse=True)
        for heading in headings:
            query = re.escape(heading)
            text = re.sub(query, query.replace(' ','_').replace('\\',""), text, flags=re.I)
        return text


    def preprocess_token(self, token):
        """Preprocess a token
        Args:
            token (str)
        Returns:
            str: preprocessed tokens
        """

        '''
        #Experimental: headings
        if token.isupper() and token.endswith(':'):
            return "\n" + "heading_" + token
        '''

        #Abbreviations
        if token.lower().strip(punctuation) in self.abbrevs.keys():
            return self.abbrevs[token.lower().strip(punctuation)]

        #assignment names
        elif token.lower().strip(punctuation) in self.hwcat.keys():
            return "{}_{}".format(self.hw_cat[token.lower().strip(punctuation)].upper(), token.upper())

        elif token.lower() in self.test_cat.keys():
            return "{}_{}".format(self.test_cat[token.lower().strip(punctuation)].upper(), token.upper())

        #Doses
        elif re.match(r"\d{1,}mg(\.?)", token, re.I):
            return "dose_{}".format(token.upper())

        #Ages
        elif re.match(r"(\d{1,2})yo", token, re.I):
            return "age_{}".format(token)

        #Durations
        elif re.match(r"(\d{1,2})yrs", token, re.I):
            return "duration_{}".format(token)

        #Dates
        elif re.match(r"\d{1,2}\/\d{1,2}(\/\\d{1,4})?", token, re.I):
            return "date_{}".format(token)

        #Times
        elif re.match(r"(@)?\d{1,2}(am|pm)", token) or re.match(r"(@)?\d{1,2}:\d{1,2}(am|pm)?", token, re.I):
            return "time_{}".format(token)

        #Tabs
        #elif re.match(r"\t\t", token):
            #return "\n\n"

        #None of the above
        else:
            return token

    def preprocess_text(self, text, lower=False):
        """Preprocess text
        Args:
            text (str)
        Returns:
            list: preprocessed tokens
        """
        preprocessed = list()

        #experimental: change multiple spaces to two newlines
        #text = re.sub(r"\s{2,}","\n\n",text)

        #experimental: try to break up headings not separated by newline
        #text = re.sub(r"([\s]+)([A-z]+:)",r"\n\n\2",text)

        text = self.join_headings(text)
        #Split at single newline but keep multiple newlines
        split = re.findall(r'\S+|\n',text)
        if lower:
            tokens = [token.lower() for token in split]
        else:
            tokens = [token for token in split]
        counter = 0
        while counter < len(tokens):
            #print("{}/{}".format(counter, len(tokens))) #for debugging
            token = self.preprocess_token(tokens[counter])
            #Collocations
            if counter < len(tokens) - 1:
                next_token = self.preprocess_token(tokens[counter+1])

                if (token + ' ' + next_token) in self.collocations:
                    preprocessed.append(token + "_" + next_token)
                    counter += 2 #skip the next word
                else:
                    preprocessed.append(token)
                    counter += 1
            else:
                preprocessed.append(token)
                counter += 1
        return preprocessed
