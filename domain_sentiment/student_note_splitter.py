# -*- coding: utf-8 -*-
"""
Script for splitting student notes into individual notes.

@author: Nicholas A Miller
"""

import re
import os

class StudentNoteSplitter:
    """Takes a .txt file with all the student's notes, and separates"""
    def __init__(self, source_dir=None):
        self.source_dir = source_dir
        self.file_pattern = re.compile(r"<FILENAME: (.*\.sn)>")

    def split_files(self, text_file,dest_dir):
        """Split a big .txt file with <ENDFILE> and <FILENAME> tags"""
        unknown_count = 0
        raw = open(text_file,errors='ignore').read()
        docs = raw.split('<ENDFILE>')
        docs = [doc for doc in docs if not doc.isspace()]
        print("Checking {} files".format(len(docs)))
        for doc in docs:
            filename = self.file_pattern.search(doc)
            try:
                print("Writing {}".format(filename[1]))
                dest_path = os.path.join(dest_dir,filename[1])
                if os.path.exists(dest_path):
                    old_path = dest_path
                    dest_path = dest_path.replace('.sn','b.sn')
                    print("{} detected. Writing {}".format(old_path, dest_path))
                with open(dest_path,'w') as dest:
                    dest.write(doc)
            except TypeError:
                with open(os.path.join(dest_dir,"unknown_{}.sn".format(str(unknown_count))),'w') as dest:
                    dest.write(doc)

    def split_dir(self, source_dir,dest_dir):
        """Split all the files in a directory"""
        for root,dirs,files in os.walk(source_dir):
            for filename in files:
                self.split_files(os.path.join(root,filename),dest_dir)
