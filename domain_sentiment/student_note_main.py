# -*- coding: utf-8 -*-
"""
Toolkit for performing domain-level sentiment analysis

The pipeline is as follows:

1. Start with one large .txt file per student.
The .txt file contains all relevant documents, separated by <ENDFILE>,
with the filename given as <FILENAME: StudentName_YYYY.MM.DD_type.sn>
It is also assumed that key headings (e.g. "Assessment Results") are given.

2. StudentNoteSplitter splits the notes into individual files

3. StudentNoteCorpus preprocesses and writes to .csv database

4. StudentNoteDatabases analyzes domain (thinking, quality, effort etc.) and
trajectory in that domain (e.g. positive or negative)

Created on Thu Jul 20 13:17:09 2017

@author: Nicholas A Miller
"""

from nltk import sent_tokenize
from student_note_splitter import StudentNoteSplitter
from student_note_corpus import StudentNoteCorpus
from student_note_database import StudentNoteDatabase

abbrevs = './abbrevs.csv'
collocations = './collocations.txt'
assignments = './assignments.csv'
headings = './headings.txt'
spreadsheet_dir = './spreadsheets'
sample_vector = "./vectors.bin.gz"


if __name__ == "__main__":
    print("Splitting texts")
    sns = StudentNoteSplitter()
    sns.split_dir('./test_files/', './split_test/')
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
    print("Creating database for sentiment scores")
    db = StudentNoteDatabase(source_dir="./spreadsheet_test",vector_dir="./vectors.bin.gz",keyword_dir="./keywords.csv")
    print("Calculating topics and sentiment scores")
    db.database_demo("./sentiment_scores_allstudents.csv")
