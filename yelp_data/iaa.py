"""
Tool for calculating inter-annotator agreement on yelp reviews

@author Nicholas Miller

Input: A .csv file of each user's annotations.

How to run (arguments in parentheses are optional):

python agreement.py <input.csv> (<options>) (> <output.txt>)

<input.csv> : the path to the input .csv file
<options>:
-c : include this option if you want the script to print the tag counts
<output.txt> (optional): the file you want the results printed to.

"""
from __future__ import print_function
import argparse
import csv
import numpy
import os
import sys
import datetime
import codecs #for solving 'null byte' error when opening file
from itertools import combinations, product
from nltk.metrics.agreement import AnnotationTask
from nltk.metrics.distance import masi_distance
from nltk.metrics.distance import jaccard_distance

def get_annotation_dicts(csv_source):
    """Process double tags, assuming comment-level only
    Args:
        csv_source: path to source csv file
    Returns:
        tag_dict: a dict of the form {(file, ant): (set of tags)}
    """
    with codecs.open(csv_source, encoding='utf-8', errors='replace') as source:
        tag_dict = dict() #{(file, ant): set()}

        reader = csv.DictReader(source)
        #reader.next() #skip header
        for row in reader:
            #Get the filename, annotator, and tag
            filename = row['File']
            ant = row['Ant']
            tag = row['Tag']

            #Skip metadata, since we're assuming annotators will agree on that
            if tag is not None and tag != 'METADATA':
                #Dictionary keys are (filename, annotator)
                #Dictionary values are {set of tags}
                try:
                    tag_dict[(filename, ant)].add(tag)
                except KeyError:
                    tag_dict[(filename,ant)] = set()
                    tag_dict[(filename, ant)].add(tag)

        #Convert to frozenset since masi distance needs immutable
        for key in tag_dict.keys():
            tag_dict[key] = frozenset(tag_dict[key])

    return tag_dict

def create_annotation_task(tag_dict):
    """Creates an AnnotationTask object and loads it with data from the given
    tag_dict
    Args
        tag_dict
    Returns:
        An annotation task object with each item consisting of the annotated
        file's name combined with the sentence number or 'R' for top-level
        tags.
    """
    #Since we're dealing with sets of labels, use Jaccard or MASI for distance
    #task = AnnotationTask(distance=masi_distance)
    task = AnnotationTask(distance=jaccard_distance)

    reader = None

    for key in tag_dict.keys(): #(file, ant)
            filename = key[0] #str
            ant = key[1] #str
            tag = tag_dict[key] #frozenset of tags
            task.load_array([(ant, filename, tag)])
    return task

def per_tag_agreement(task):
    """Calculate the agreement for each label,
    e.g. for a particular label, find all the items with that label,
    then for each item with that label, find the number of times
    the item received exactly that label, and divide by all the labels for the item
    """
    for label in task.K:
        match_label = [item for item in task.data if item['labels'] == label]
        #match_label = [item for item in task.data if item['labels'].intersection(label)]
        match_label_items = set([item['item'] for item in match_label])
        match_count = len(match_label)
        total_count = 0
        for match_label_item in match_label_items:
            total_count += len([item for item in task.data if item['item'] == match_label_item])
        match_score = match_count / float(total_count)
        print("Agreement for [{}]: {}/{} ({})".format(','.join(label), match_count, total_count, match_score))

def per_tag_intersection(task):
    """Calculate the agreement for each label,
    e.g. for a particular set of labels k, find all the items with that label,
    then for each item with that label, find the number of times
    the item was given a set of labels that intersect with k, and divide by all the labels for the item
    """

    for label in task.K:
        #match_label = [item for item in task.data if item['labels'] == label]
        match_label = [item for item in task.data if item['labels'].intersection(label)]
        match_label_items = set([item['item'] for item in match_label])
        match_count = len(match_label)
        total_count = 0
        for match_label_item in match_label_items:
            total_count += len([item for item in task.data if item['item'] == match_label_item])
        match_score = match_count / float(total_count)
        print("Intersection agreement for [{}]: {}/{} ({})".format(','.join(label), match_count, total_count, match_score))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Calculate IAA')
    parser.add_argument('source')
    parser.add_argument('-c', '--counts', action='store_true')
    parser.add_argument('-a', '--agreement', action='store_true')

    args = parser.parse_args()

    if not (args.counts):
        print_counts = False
        print_agreement = False
    else:
        print_counts = args.counts
        print_agreement = args.agreement

    source_path = args.source
    tag_dict = get_annotation_dicts(source_path)
    tag_task = create_annotation_task(tag_dict)
    #Find missing tags
    missing = list()
    for filename in tag_task.I:
        for ant in tag_task.C:
            if (filename, ant) not in tag_dict.keys():
                missing.append((filename, ant))
                print("Filling in default value for ({}, {})".format(filename, ant))
                tag_dict[(filename, ant)] = (frozenset(['NONE']))
    tag_task = create_annotation_task(tag_dict)
    print("\n")

    tasks = {'tag': tag_task}
    for task in tasks.keys():
        if print_counts:
            print("{} counts for all annotators:".format(task))
            for tag in tasks[task].K:
                print("{}: {}".format(','.join(tag), str(int(tasks[task].Nk(tag)))))
            print("\n")
        if print_agreement:
            per_tag_agreement(tasks[task])
            print()
            per_tag_intersection(tasks[task])
            print()
        annotator_pairs = combinations(tasks[task].C, 2)
        print("{} Agreement statistics (Comment-level)".format(task))
        for c1, c2 in annotator_pairs:
            print("Agreement between {} and {}: {}".format(c1, c2, tasks[task].Ao(c1, c2)))
        print("Pi: {}".format(tasks[task].pi()))
        print("Alpha: {}".format(tasks[task].alpha()))
        print("Kappa: {}".format(tasks[task].kappa()))
        print("\n")
