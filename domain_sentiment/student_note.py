# -*- coding: utf-8 -*-
"""
Object representing student notes

Created on Thu Jul 20 12:57:41 2017

@author: Nicholas A Miller
"""

import dateutil
import dateutil.parser
import re, os
from nltk.tokenize.punkt import PunktSentenceTokenizer
import nltk

def try_date(s):
    """
    Check whether a string is a date
    Args:
        s (string): string to check
    Returns:
        datetime: if it's a date, None if it's not a date
    """
    try:
        parsed = dateutil.parser.parse(s)
        return parsed
    except ValueError:
        return None

class StudentNote:
    """
    Class representing student notes

    Attributes:
        filepath (string): path to the file
        student_name (string): name of the student
        note_date (datetime): date the record was written
        note_type (string): type of student note
    Methods:
        is_complete(): checks whether student note is complete
        __str__(): override default
        __repr(): override default
    """
    def __init__(self, filename):
        """Constructor: load the date, name, type from filename
        Args:
            filename (string): path to file
        Assumes filename format StudentName_YYYY.MM.DD_Type.cn
        """
        filename_split = os.path.basename(filename).split('_')
        #filename_split = filename.split('_')
        self.filepath = filename
        self.text = None
        self.student_name = None
        self.note_date = None
        self.note_type = None
        #self.tiling = my_tile.TextTilingTokenizer()

        for segment in filename_split:
            is_date = try_date(segment)
            if is_date:
                self.note_date = is_date
            elif re.match(r'[A-Z][a-z]+[A-Z][a-z]+', segment):
                self.student_name = segment
            else:
                self.note_type = segment

    def is_complete(self):
        """
        Is it a complete record?
        Returns:
            boolean
        """
        return (self.student_name and self.note_date and self.note_type)

    def load_text(self):
        """Load the text of the StudentNote
        """
        try:
            self.text = open(self.filepath).read()
        except Exception as e:
            print("Error: {}".format(e))

    def search_note(self, term):
        """Search StudentNote object for given term, returning sentences
        Assumes note text has been loaded and preprocessed
        Args:
            term (str): term to look for
        Returns:
            list of ((date, sent, type)) tuples
        """
        result = list()
        try:
            '''
            if not self.text:
                #Load text if it hasn't already been loaded
                self.load_text()
            pre = pp.Preprocessor('abbrevs.csv','collocations.txt','meds.csv')
            ppd = ' '.join(pre.preprocess_text(self.text))
            ppd = ' '.join(pre.preprocess_text(ppd)) #one more time to get what we missed
            '''
            for sent in nltk.sent_tokenize(self.text):
                if re.search(term, sent, re.I):
                    result.append((self.note_date, sent, self.note_type))
            return sorted(result, key= lambda x: x[0]) #sort by date
        except Exception as e:
            print(e)


    def set_filepath(self, newpath):
        self.filepath = newpath

    def __str__(self):
        return "[Name: {}, Date: {}, Type: {}]".format(self.student_name, self.note_date, self.note_type)

    def __repr__(self):
        return "[Name: {}, Date: {}, Type: {}]".format(self.student_name, self.note_date, self.note_type)
