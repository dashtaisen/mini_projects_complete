# -*- coding: utf-8 -*-
"""
Script for creating a database from student note spreadsheets,
and performing domain and trajectory evaluation.

@author: Nicholas A Miller
"""

import os,csv
from string import punctuation
from nltk import sent_tokenize

class StudentNoteDatabase():
    """Represents a database with the keys as students
    and the values as all csv rows for OnTrack notes for that student"""
    def __init__(self,source_dir=None,vector_dir=None,keyword_dir=None,maxsize=100000):
        self.records = dict()
        self.model = None
        self.whitelists = dict() #{'domain':{words}}
        self.blacklists = dict() #{'domain':{words}}
        self.positive_words = dict() #{'domain':{words}}
        self.negative_words = dict() #{'domain':{words}}

        if keyword_dir:
            self.load_lists(keyword_dir)

        if source_dir:
            self.load_records(source_dir)

        if vector_dir:
            self.model = self.load_embeddings(vector_dir,maxsize)

        print(self.whitelists)
        print(self.blacklists)
        print(self.positive_words)
        print(self.negative_words)

    def load_lists(self, keyword_dir):
        """Load whitelists, blacklists, positive words, and negative words"""
        reader = csv.DictReader(open(keyword_dir))
        topics = [row["Domain"] for row in reader]
        reader = csv.DictReader(open(keyword_dir))
        for topic in topics:
            self.whitelists[topic] = set()
            self.blacklists[topic] = set()
            self.positive_words[topic] = set()
            self.negative_words[topic] = set()
        for row in reader:
            if row["List"] == "whitelist":
                self.whitelists[row["Domain"]].add(row["Word"])
                if row["Sentiment"] == "positive":
                    self.positive_words[row["Domain"]].add(row["Word"])
                elif row["Sentiment"] == "negative":
                    self.negative_words[row["Domain"]].add(row["Word"])
            elif row["List"] == "blacklist":
                self.blacklists[row["Domain"]].add(row["Word"])

    def load_records(self,source_dir):
        #Populate the fields
        self.records= dict()
        if source_dir:
            for root, dirnames, filenames in os.walk(source_dir):
                for filename in filenames:
                    pname = filename[:filename.find('_')]
                    with open(os.path.join(root,filename)) as f:
                        reader = csv.DictReader(f)
                        self.records[pname] = list()
                        for row in reader:
                            self.records[pname].append(row)

    def load_embeddings(self, vectors, maxsize=100000):
        #Put import statement here to save time
        #i.e. don't bother importing gensim if we're not using a model
        from gensim.models.keyedvectors import KeyedVectors
        model = KeyedVectors.load_word2vec_format(vectors, binary=True,limit=maxsize)
        return model

    def field_from_student(self,student,field):
        """Get a list of texts from the given student and the given field"""
        return [row["Text"] for row in self.records[student] if row["Field"] == field]

    def field_from_all(self,field):
        """Get a list of texts from all students and the given field"""
        return [row["Text"] for student in self.records.keys() for row in self.records[student] if row["Field"] == field]

    def field_pars(self,field):
        """Get a string of all texts from all students and the given field, separated by two newlines"""
        return '\n\n'.join(self.field_from_all(field))

    def field_pars_unique(self,field):
        """Get a string of all unique texts from all students and the given field, separated by two newlines"""
        return '\n\n'.join(set(self.field_from_all(field)))

    def get_sentences_by_topic(self, pname):
        """Get sentences about a particular topic"""
        sents_by_topic = dict()
        topics = set([key for key in self.whitelists.keys() if key != 'general'])
        for row in self.records[pname]:
            date = row["Date"].split()[0] #hack to get rid of time, TODO: adjust this earlier in the pipeline
            text = row["Text"]
            field = row["Field"]
            row_type = row["Type"]
            if field not in {"plan","goals"}: #Ignore "plan" fields, to reduce noise
            #if field in {"current_information","current_information/session_content","notes","problems","new_information"}:
                for sent in sent_tokenize(text):
                    topic_choice = None
                    #print(sent) #for debugging
                    topic_score = dict()
                    #We're going to decide the topic based on the unique words in the sentence
                    #We call them 'tokens' here, but CL folks call them 'types'
                    tokens = set([word.strip(punctuation) for word in sent.lower().split()])
                    #Sentence contains at least one word from the whitelist and none from the blacklist
                    for token in tokens:
                        for topic in topics:
                            if token in self.whitelists[topic]:
                                topic_score[topic] = topic_score.get(topic, 0) + 1
                            elif token in self.blacklists[topic]:
                                topic_score[topic] = topic_score.get(topic, 0) - 1
                    #Normalize scores -- prioritizes precision over recall
                    if len(topic_score.keys()) >0:
                        #for topic in topic_score.keys():
                            #topic_score[topic] = topic_score[topic] / len(sent)
                        topic_choice = max(topic_score, key=lambda x: topic_score[x])
                        topic_choice_score = topic_score[topic_choice]
                    #Have a threshold for topic scores
                        #print("{}:{}".format(sent, topic_score))
                    if topic_choice != None and topic_choice_score > 0:
                        try:
                            sents_by_topic[topic_choice].append((pname, date, field, row_type, sent,topic_choice_score))
                        except KeyError:
                            sents_by_topic[topic_choice] = [(pname, date, field, row_type, sent,topic_choice_score)]
        return sents_by_topic

    def get_sentiments_by_topic(self, pname):
        '''Assign sentiment score to a text'''

        #Can't do anything if we haven't loaded a word embedding model
        if not self.model:
            print("Model not loaded.")
            return None
        else:
            #Stopwords are function words such as 'of', 'the,' is' etc.,
            #which we typically ignore
            from gensim.parsing.preprocessing import STOPWORDS
            from gensim.utils import simple_preprocess
            sentences_by_topic = self.get_sentences_by_topic(pname)
            topics = list(sentences_by_topic.keys())
            sentiments_by_topic = dict()
            for topic in topics:
                sentiments_by_topic[topic] = list()
                for sentence in sentences_by_topic[topic]:
                    name, date, field, note_type, text,topic_score = sentence[:6]
                    #Start with a score of 0.
                    score = 0
                    denial = False #"denies"
                    reduce_strength = False #"less", "not as"
                    #Look at all the words in the text except function words ('a','of','the',etc.)
                    if "denies" in text.lower() or "no history of" in text.lower():
                        denial = True
                    if "less" in text.lower() or "not as" in text.lower():
                        reduce_strength = True
                    tokens = [token for token in simple_preprocess(text) if token not in STOPWORDS]
                    for token in tokens:
                        try:
                            #Add to the overall score based on postiveness and negativeness of the word
                            #similarity will be a number between 0 and 1
                            #TODO: consider having more axes than just positive and negative
                            #TODO: consider having different axes depending on the topic
                            #e.g. mania, depression, happiness, sadeness, anxiety for mood
                            for pos_word in self.positive_words['general']:
                                similarity = self.model.similarity(token, pos_word)
                                if similarity > .5:
                                    score += similarity
                            for neg_word in self.negative_words['general']:
                                similarity = self.model.similarity(token, neg_word)
                                if similarity > .5:
                                    score -= similarity
                            for pos_word in self.positive_words[topic]:
                                similarity = self.model.similarity(token, pos_word)
                                if similarity > .5:
                                    score += similarity
                            for neg_word in self.negative_words[topic]:
                                similarity = self.model.similarity(token, neg_word)
                                if similarity > .5:
                                    score -= similarity

                        except KeyError: #handle out-of-vocabulary items
                            score += 0
                    if denial:
                        score = 0
                    if reduce_strength:
                        score = .5 * score
                    sentiments_by_topic[topic].append((name, date, field, note_type, text, topic_score, score))
            return sentiments_by_topic


    def database_demo(self,dest_file):
        """Demonstrate topic selection and sentiment scoring"""
        with open(dest_file,'w',newline='') as dest:
                writer = csv.DictWriter(dest, fieldnames=["Student", "Date", "Field","Type", "Text","Domain","Domain Score","Sentiment"])
                writer.writeheader()
        for pname in self.records.keys():
            sentiments_by_topic = self.get_sentiments_by_topic(pname) #student, date, type, text
            with open(dest_file,'a',newline='') as dest:
                writer = csv.DictWriter(dest, fieldnames=["Student", "Date", "Field","Type", "Text","Domain","Domain Score", "Sentiment"])
                for topic in sentiments_by_topic.keys():
                    for result in sentiments_by_topic[topic]:
                        row = dict()
                        row["Student"] = result[0]
                        row["Date"] = result[1]
                        row["Field"] = result[2]
                        row["Type"] = result[3]
                        row["Text"] = result[4]
                        row["Domain"] = topic
                        row["Domain Score"] = result[5]
                        row["Sentiment"] = result[6]
                        writer.writerow(row)
