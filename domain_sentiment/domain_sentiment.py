# -*- coding: utf-8 -*-
"""
Toolkit for performing domain-level sentiment analysis

Created on Thu Jul 20 13:17:09 2017

@author: Nicholas A Miller
"""

abbrevs = './abbrevs.csv'
collocations = './collocations.txt'
assignments = './assignments.csv'
headings = './unique_headings.txt'
spreadsheet_dir = './spreadsheets'
sample_vector = "./vectors.bin.gz"

from nltk import sent_tokenize

import os, sys, re
import time
import csv
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import random #for choosing random students and notes
import datetime
from string import punctuation #for stripping trailing punctuation
import student_note as sn
import student_note_splitter as splitter






if __name__ == "__main__":
    """
    print("Splitting texts")
    sns = StudentNoteNoteSplitter()
    sns.split_dir('./text_files/', './split_test/')
    print("Loading corpus")
    snc = StudentNoteCorpus('./split_test')
    print("Loaded corpus with {} students".format(len(snc.notes.keys())))
    snc.load_all_texts()
    snc.load_preprocessor(abbrevs, collocations, assignments, headings)
    print("Joining headings")
    for student in snc.notes.keys():
        print("Processing {}".format(student))
        for note in snc.notes[student]:
            note.text = snc.preprocessor.join_headings(note.text)
    print("Writing csv files")
    for student in snc.notes.keys():
        print("Writing csv for {}".format(student))
        snc.make_heading_csv(student,'./spreadsheet_test')
    """
    print("Creating database for sentiment scores")
    db = StudentNoteDatabase(source_dir="./spreadsheet_test")
    print("Calculating topics and sentiment scores")
    db.database_demo("./sentiment_scores_allstudents.csv")
