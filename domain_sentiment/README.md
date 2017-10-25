# Corpus sentiment analysis tools

Nicholas Miller

## Description

This is a collection of tools that I've used to process documents in various formats, and then perform sentiment analysis on them.

I was a teacher before starting the CL MA program, so I was thinking in particular of applications to educational documents (teacher's comments on student work, quarterly evaluations, etc.), but the overall framework could be applied to other kinds of documents.

## Data Pipeline

The pipeline is as follows:

1. Start with one large .txt file per student.
The .txt file contains all relevant documents, separated by <ENDFILE>,
with the filename given as <FILENAME: StudentName_YYYY.MM.DD_type.sn>
It is also assumed that key headings (e.g. "Assessment Results") are given. See, for example, the file in the test_files folder.

2. StudentNoteSplitter splits the notes into individual files.

3. StudentNoteCorpus preprocesses each document, and can write the files to .csv (in case you want to manipulate them using, say, Excel or Pandas).

4. StudentNoteDatabases analyzes domain (thinking, quality, effort etc.) and
trajectory in that domain (e.g. positive or negative)
