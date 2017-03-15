"""
Yelp review text segmenter
"""

import json
import pickle
import yelp_dataset_tools

#replace this with the directory of your business JSON file

yelp_path = '../../yelp/yelp_dataset_challenge_round9/'

business_path = yelp_path + 'yelp_academic_dataset_business.json'

class ReviewSegmenter(YelpParser):
    """Class for working with JSON of yelp reviews"""
    def __init__(self, source_path):
        YelpParser.__init__(self, source_path)

    def get_data_from_json(self):
        """Load data from source path as a JSON data object"""
        #Input: JSON file
        #Output: JSON object
        #We don't use loads() because it's dumped as json, not string
        with open(self.source) as f:
            data = json.load(f)        
        return data

