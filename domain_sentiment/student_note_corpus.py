# -*- coding: utf-8 -*-
"""
Script for creating a corpus of student note files

@author: Nicholas A Miller
"""

from student_note_preprocessor import StudentNotePreprocessor
from collections import defaultdict
import os,re,csv
import student_note as sn

class StudentNoteCorpus:
    def __init__(self, source_dir):
        #self.notes is a dict {student: [list of StudentNote objects]}
        self.notes = self.compile_notes(source_dir)
        self.preprocessor = None


    def load_preprocessor(self, abbrevs, collocations, assignments, headings):
        """Load the preprocessor"""
        self.preprocessor = StudentNotePreprocessor(abbrevs, collocations, assignments, headings)

    def compile_notes(self, source_dir):
        """
        Recursively explore directory and compile StudentNote objects
        Args:
            source_dir (string): path to directory
        """
        notes = defaultdict(list)
        for root, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                if filename.endswith('.sn'):
                    #note = cn.StudentNote(os.path.join(os.path.realpath(root), filename))
                    note = sn.StudentNote(os.path.join(os.path.realpath(root), filename))
                    if note.is_complete():
                        notes[note.student_name].append(note)
                    else:
                        pass
                        #print("Skipping incomplete note") #for debugging
        return notes

    def get_headings_for_student(self, student):
        raw_headings = sorted([heading.strip().replace(' ','_') for heading in self.preprocessor.headings], key= lambda x:len(x), reverse=True)

        headings = list()
        for heading in raw_headings:
            if not heading.endswith(':'):
                headings.append(heading + '\n')
            else:
                headings.append(heading)
        #print(headings)
        heading_dict = dict()
        notes = self.notes[student]
        for note in notes:
            text = note.text
            tokens = re.findall(r'\S+|\n',text)
            current_key = "NO_KEY"
            #previous_key = "NO_KEY"
            current_utterance = list()
            for token in tokens:
                if token in headings:
                    if current_utterance is not None:
                        try:
                            heading_dict[current_key].append((note.student_name, note.note_date, note.note_type, ' '.join(current_utterance)))
                        except KeyError:
                            heading_dict[current_key] = list()
                            heading_dict[current_key].append((note.student_name, note.note_date, note.note_type, ' '.join(current_utterance)))
                    current_key = token
                    current_utterance = list()
                else:
                    current_utterance.append(token)
            if current_utterance: #We haven't added the last heading matches yet
                try:
                    heading_dict[current_key].append((note.student_name, note.note_date, note.note_type, ' '.join(current_utterance)))
                except KeyError:
                    heading_dict[current_key] = list()
                    heading_dict[current_key].append((note.student_name, note.note_date, note.note_type, ' '.join(current_utterance)))
        return heading_dict

    def make_heading_csv(self, student, dest_dir):
        fields = ["Name", "Field", "Date", "Type", "Text"]
        heading_dict = self.get_headings_for_student(student)
        filename = os.path.join(dest_dir, "{}_headings.csv".format(student))
        with open(filename, 'w', newline='') as dest:
            writer = csv.DictWriter(dest,fieldnames=fields)
            writer.writeheader()
            for key in heading_dict.keys():
                for result in heading_dict[key]:
                    row = dict()
                    row["Name"] = result[0]
                    row["Field"] = key
                    row["Date"] = result[1]
                    row["Type"] = result[2][:-3]
                    row["Text"] = result[3].strip()
                    if len(row["Text"]) >0:
                        writer.writerow(row)


    def search_all(self, term):
        """Search StudentNote objects for given term, returning sentences
        Assumes text has been loaded and preprocessed

        Args:
            student (str): name of student
            term (str): term to look for
        Returns:
            list of ((student, date, match, type)) tuples
        """
        results = list()
        for student in self.notes.keys():
            result = self.search_student(student, term)
            for r in result:
                results.append((student, r[0], r[1], r[2]))
        return sorted(results, key= lambda x: x[0]) #sort by date


    def search_all_span(self, term, offset=20):
        """Search StudentNote objects for given term, returning sentences
        Assumes text has been loaded and preprocessed
        Args:
            student (str): name of student
            term (str): term to look for
            offset (int): how many chars before and after
        Returns:
            list of ((student, date, match, type)) tuples
        """
        result = list()
        for student in self.notes.keys():
            student_notes = self.notes[student]
            for note in student_notes:
                '''
                if not note.text:
                    #Load text if it hasn't already been loaded
                    note.load_text()
                '''
                for match in re.finditer(term, note.text, re.I):
                    #Get the string plus offset (a few chars before and after)
                    lindex, rindex = match.span()[0]-offset, match.span()[1]+offset
                    result.append((note.student_name, note.note_date, note.text[lindex:rindex], note.note_type))
        return sorted(result, key= lambda x: x[0]) #sort by date


    def search_student(self, student, term):
        """Search StudentNote objects for given term, returning sentences
        Assumes text has been loaded and preprocessed
        Args:
            student (str): name of student
            term (str): term to look for
        Returns:
            list of ((date, sent, type)) tuples
        """
        result = list()
        try:
            student_notes = self.notes[student]
            for note in student_notes:
                '''
                if not note.text:
                    #Load text if it hasn't already been loaded
                    note.load_text()
                '''
                '''
                if not self.preprocessor:
                    self.load_preprocessor('abbrevs.csv','collocations.txt','assignments.csv')
                ppd = ' '.join(self.preprocessor.preprocess_text(note.text))
                ppd = ' '.join(self.preprocessor.preprocess_text(ppd)) #one more time to get what we missed
                '''
                paragraphs = note.text.split('\n')
                for paragraph in paragraphs:
                    for sent in nltk.sent_tokenize(paragraph):
                        if re.search(term, sent, re.I):
                            result.append((note.note_date, sent, note.note_type))
            return sorted(result, key= lambda x: x[0]) #sort by date
        except Exception as e:
            print(e)

    def search_student_span(self, student, term, offset=20):
        """Search StudentNote objects for given term, returning spans of text
        Args:
            student (str): name of student
            term (str): term to look for
            offset (int): how many chars before and after
        Returns:
            list of ((date, match, type)) tuples
        """
        result = list()
        try:
            student_notes = self.notes[student]
            for note in student_notes:
                '''
                if not note.text:
                    #Load text if it hasn't already been loaded
                    note.load_text()
                '''
                for match in re.finditer(term, note.text, re.I):
                    #Get the string plus offset (a few chars before and after)
                    lindex, rindex = match.span()[0]-offset, match.span()[1]+offset
                    result.append((note.note_date, note.text[lindex:rindex], note.note_type))
            return sorted(result, key= lambda x: x[0]) #sort by date
        except Exception as e:
            print(e)


    def random_student(self):
        """Get a random student
        Returns:
            str: student name
        """
        return random.choice(list(self.notes.keys()))

    def random_note(self, student=None):
        """Get a random note from a specified or random student
        Args:
            student (str): student's name
        Returns:
            StudentNote
        """
        if student:
            note = random.choice(self.notes.get(student))
            return note
        else:
            note = random.choice(self.notes.get(random.choice(list(self.notes.keys()))))
            return note

    def load_all_texts(self):
        """Load the text for all Student notes"""
        for student in self.notes.keys():
            for note in self.notes[student]:
                note.load_text()

    def preprocess_all_texts(self):
        """Load and preprocess all the texts in the Student note corpus
        """
        for student in self.notes.keys():
            for note in self.notes[student]:
                if not note.text:
                    note.load_text()
                preprocessed = ' '.join(self.preprocessor.preprocess_text(note.text))
                #preprocessed = ' '.join(preprocessor.preprocess_text(preprocessed))
                preprocessed = preprocessed.replace('\n \n', '\n\n')
                note.text = preprocessed

    def write_preprocessed(self, destdir):
        #Replace this with more thorough preprocessing later
        for student in self.notes.keys():
            for note in self.notes[student]:
                filename = "{}_{}_{}.preproc".format(note.student_name, note.note_date.strftime("%Y%m%d"), note.note_type)
                filepath = os.path.join(destdir,filename)
                with open(filepath,'w') as dest:
                    dest.write(self.preprocessor.join_headings(note.text))
